import time

cache = {}

def spam(uid):
    now = time.time()
    cache.setdefault(uid, [])
    cache[uid].append(now)
    cache[uid] = [t for t in cache[uid] if now - t < 5]
    return len(cache[uid]) > 5

def caps(msg):
    if len(msg) < 10:
        return False
    return sum(1 for c in msg if c.isupper()) / len(msg) > 0.7

def links(msg):
    return "http://" in msg or "https://" in msg
