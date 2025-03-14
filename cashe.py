from aiocache import Cache

# Uses aiocache to store user posts in memory for 5 minutes.
#     Avoids repeated database calls by checking the cache before querying the database.

cache = Cache.from_url("memory://")

def get_from_cache(user_id: int):
    return cache.get(f"posts:{user_id}")

def cache_to_memory(user_id: int, posts: list):
    cache.set(f"posts:{user_id}", posts, ttl=300)  # TTL = 300 секунд = 5 хвилин
