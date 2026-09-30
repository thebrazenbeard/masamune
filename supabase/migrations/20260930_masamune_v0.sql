create table if not exists public.masamune_webhook_delivery (
    delivery_id text primary key,
    event_name text not null,
    state text not null check (
        state in (
            'ACCEPTED',
            'PROCESSING',
            'READY_TO_PUBLISH',
            'COMPLETED',
            'FAILED',
            'IGNORED'
        )
    ),
    received_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    payload_sha256 text not null,
    error text
);

create table if not exists public.masamune_review_receipt (
    review_id text primary key,
    delivery_id text not null references public.masamune_webhook_delivery(delivery_id),
    repository text not null,
    subject_kind text not null check (
        subject_kind in ('PULL_REQUEST', 'ISSUE', 'SWEEP')
    ),
    subject_number bigint,
    head_sha text not null,
    result_json jsonb not null,
    created_at timestamptz not null default now()
);

create index if not exists masamune_review_receipt_repository_idx
    on public.masamune_review_receipt (repository, created_at desc);

alter table public.masamune_webhook_delivery enable row level security;
alter table public.masamune_review_receipt enable row level security;

comment on table public.masamune_webhook_delivery is
    'Masamune webhook idempotency and processing lifecycle. Service role only; no public RLS policy.';

comment on table public.masamune_review_receipt is
    'Exact-subject Masamune review receipts. Service role only; no public RLS policy.';


create table if not exists public.masamune_daily_usage (
    usage_day date primary key,
    review_count integer not null default 0 check (review_count >= 0)
);

create table if not exists public.masamune_repo_daily_usage (
    repository text not null,
    usage_day date not null,
    review_count integer not null default 0 check (review_count >= 0),
    primary key (repository, usage_day)
);

create table if not exists public.masamune_review_budget_claim (
    review_id text primary key,
    repository text not null,
    usage_day date not null,
    claimed_at timestamptz not null default now()
);

alter table public.masamune_daily_usage enable row level security;
alter table public.masamune_repo_daily_usage enable row level security;
alter table public.masamune_review_budget_claim enable row level security;

create or replace function public.masamune_claim_review_budget(
    p_review_id text,
    p_repository text,
    p_global_limit integer,
    p_repo_limit integer
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
    v_day date := (now() at time zone 'utc')::date;
    v_global integer;
    v_repo integer;
begin
    if p_global_limit < 1 or p_repo_limit < 1 then
        return false;
    end if;

    perform pg_advisory_xact_lock(hashtext('masamune-budget-' || v_day::text));

    if exists (
        select 1
        from public.masamune_review_budget_claim
        where review_id = p_review_id
    ) then
        return true;
    end if;

    insert into public.masamune_daily_usage (usage_day, review_count)
    values (v_day, 0)
    on conflict (usage_day) do nothing;

    insert into public.masamune_repo_daily_usage (repository, usage_day, review_count)
    values (p_repository, v_day, 0)
    on conflict (repository, usage_day) do nothing;

    select review_count into v_global
    from public.masamune_daily_usage
    where usage_day = v_day
    for update;

    select review_count into v_repo
    from public.masamune_repo_daily_usage
    where repository = p_repository and usage_day = v_day
    for update;

    if v_global >= p_global_limit or v_repo >= p_repo_limit then
        return false;
    end if;

    insert into public.masamune_review_budget_claim (
        review_id,
        repository,
        usage_day
    )
    values (p_review_id, p_repository, v_day);

    update public.masamune_daily_usage
    set review_count = review_count + 1
    where usage_day = v_day;

    update public.masamune_repo_daily_usage
    set review_count = review_count + 1
    where repository = p_repository and usage_day = v_day;

    return true;
end;
$$;

revoke all on function public.masamune_claim_review_budget(text, text, integer, integer)
    from public, anon, authenticated;
grant execute on function public.masamune_claim_review_budget(text, text, integer, integer)
    to service_role;

comment on function public.masamune_claim_review_budget(text, text, integer, integer) is
    'Atomically admits one idempotent zero-cost review within UTC global and per-repository daily caps.';


create table if not exists public.masamune_execution_lease (
    singleton_id smallint primary key check (singleton_id = 1),
    review_id text,
    leased_until timestamptz
);

insert into public.masamune_execution_lease (
    singleton_id,
    review_id,
    leased_until
)
values (1, null, null)
on conflict (singleton_id) do nothing;

alter table public.masamune_execution_lease enable row level security;

create or replace function public.masamune_claim_execution_lease(
    p_review_id text,
    p_ttl_seconds integer
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
    v_review_id text;
    v_leased_until timestamptz;
begin
    if p_ttl_seconds < 30 or p_ttl_seconds > 600 then
        return false;
    end if;

    select review_id, leased_until
    into v_review_id, v_leased_until
    from public.masamune_execution_lease
    where singleton_id = 1
    for update;

    if v_review_id = p_review_id then
        update public.masamune_execution_lease
        set leased_until = now() + make_interval(secs => p_ttl_seconds)
        where singleton_id = 1;
        return true;
    end if;

    if v_review_id is null or v_leased_until is null or v_leased_until <= now() then
        update public.masamune_execution_lease
        set
            review_id = p_review_id,
            leased_until = now() + make_interval(secs => p_ttl_seconds)
        where singleton_id = 1;
        return true;
    end if;

    return false;
end;
$$;

create or replace function public.masamune_release_execution_lease(
    p_review_id text
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
    v_updated integer;
begin
    update public.masamune_execution_lease
    set review_id = null, leased_until = null
    where singleton_id = 1 and review_id = p_review_id;

    get diagnostics v_updated = row_count;
    return v_updated = 1;
end;
$$;

revoke all on function public.masamune_claim_execution_lease(text, integer)
    from public, anon, authenticated;
grant execute on function public.masamune_claim_execution_lease(text, integer)
    to service_role;

revoke all on function public.masamune_release_execution_lease(text)
    from public, anon, authenticated;
grant execute on function public.masamune_release_execution_lease(text)
    to service_role;

comment on table public.masamune_execution_lease is
    'Single zero-cost model-execution lease used to avoid concurrent free-tier quota bursts.';

comment on function public.masamune_claim_execution_lease(text, integer) is
    'Claims or renews the singleton Masamune model-execution lease with expiry.';

comment on function public.masamune_release_execution_lease(text) is
    'Releases the singleton Masamune model-execution lease only for its current review owner.';
