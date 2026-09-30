def get_profile(user_id, tenant_id, cache):
    cached = cache[user_id]
    if cached is not None:
        return cached
    return load_profile(tenant_id, user_id)