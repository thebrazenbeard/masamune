def send_with_retry(send):
    for attempt in range(3):
        try:
            return send()
        except TimeoutError:
            if attempt == 2:
                raise

    raise RuntimeError("unreachable")