const encoder = new TextEncoder();

function asArrayBuffer(bytes: Uint8Array): ArrayBuffer {
  return bytes.buffer.slice(
    bytes.byteOffset,
    bytes.byteOffset + bytes.byteLength,
  ) as ArrayBuffer;
}

export function base64Url(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replaceAll("+", "-").replaceAll("/", "_").replace(
    /=+$/g,
    "",
  );
}

function decodePemBody(pem: string): { label: string; der: Uint8Array } {
  const match = pem.trim().match(
    /^-----BEGIN ([A-Z ]+)-----\s*([A-Za-z0-9+/=\s]+)\s*-----END \1-----$/,
  );
  if (!match) throw new Error("invalid PEM private key");
  const binary = atob(match[2].replace(/\s+/g, ""));
  const der = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) der[i] = binary.charCodeAt(i);
  return { label: match[1], der };
}

function derLength(length: number): Uint8Array {
  if (length < 0x80) return new Uint8Array([length]);
  const bytes: number[] = [];
  let value = length;
  while (value > 0) {
    bytes.unshift(value & 0xff);
    value >>= 8;
  }
  return new Uint8Array([0x80 | bytes.length, ...bytes]);
}

function der(tag: number, payload: Uint8Array): Uint8Array {
  const len = derLength(payload.length);
  const out = new Uint8Array(1 + len.length + payload.length);
  out[0] = tag;
  out.set(len, 1);
  out.set(payload, 1 + len.length);
  return out;
}

function concat(...parts: Uint8Array[]): Uint8Array {
  const size = parts.reduce((sum, part) => sum + part.length, 0);
  const out = new Uint8Array(size);
  let offset = 0;
  for (const part of parts) {
    out.set(part, offset);
    offset += part.length;
  }
  return out;
}

function pkcs1ToPkcs8(pkcs1: Uint8Array): Uint8Array {
  const version = new Uint8Array([0x02, 0x01, 0x00]);
  const rsaOid = new Uint8Array([
    0x30,
    0x0d,
    0x06,
    0x09,
    0x2a,
    0x86,
    0x48,
    0x86,
    0xf7,
    0x0d,
    0x01,
    0x01,
    0x01,
    0x05,
    0x00,
  ]);
  const privateKey = der(0x04, pkcs1);
  return der(0x30, concat(version, rsaOid, privateKey));
}

async function importGithubPrivateKey(pem: string): Promise<CryptoKey> {
  const parsed = decodePemBody(pem.replaceAll("\\n", "\n"));
  let keyDer: Uint8Array;
  if (parsed.label === "PRIVATE KEY") {
    keyDer = parsed.der;
  } else if (parsed.label === "RSA PRIVATE KEY") {
    keyDer = pkcs1ToPkcs8(parsed.der);
  } else {
    throw new Error(`unsupported private-key PEM label: ${parsed.label}`);
  }
  return await crypto.subtle.importKey(
    "pkcs8",
    asArrayBuffer(keyDer),
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false,
    ["sign"],
  );
}

export async function signGithubAppJwt(
  appId: string,
  privateKeyPem: string,
): Promise<string> {
  const now = Math.floor(Date.now() / 1000);
  const header = base64Url(
    encoder.encode(JSON.stringify({ alg: "RS256", typ: "JWT" })),
  );
  const payload = base64Url(
    encoder.encode(
      JSON.stringify({
        iat: now - 30,
        exp: now + 8 * 60,
        iss: appId,
      }),
    ),
  );
  const signingInput = `${header}.${payload}`;
  const key = await importGithubPrivateKey(privateKeyPem);
  const signature = new Uint8Array(
    await crypto.subtle.sign(
      "RSASSA-PKCS1-v1_5",
      key,
      encoder.encode(signingInput),
    ),
  );
  return `${signingInput}.${base64Url(signature)}`;
}

export async function sha256Hex(data: Uint8Array): Promise<string> {
  const digest = new Uint8Array(
    await crypto.subtle.digest("SHA-256", asArrayBuffer(data)),
  );
  return Array.from(digest, (byte) => byte.toString(16).padStart(2, "0")).join(
    "",
  );
}

export async function verifyGithubSignature(
  secret: string,
  body: Uint8Array,
  signature: string | null,
): Promise<boolean> {
  if (!secret || !signature?.startsWith("sha256=")) return false;
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const digest = new Uint8Array(
    await crypto.subtle.sign("HMAC", key, asArrayBuffer(body)),
  );
  const expected = `sha256=${
    Array.from(digest, (b) => b.toString(16).padStart(2, "0")).join("")
  }`;
  if (expected.length !== signature.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) {
    diff |= expected.charCodeAt(i) ^ signature.charCodeAt(i);
  }
  return diff === 0;
}
