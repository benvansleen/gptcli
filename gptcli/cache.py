import os
import json
from hashlib import sha256

CACHE_FILE = '/tmp/cache.json'
MAX_CACHE_SIZE = 20
cur_cache = {}


def init_cache():
    global cur_cache
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w') as f:
            json.dump({'hash': 'response'}, f)

    else:
        with open(CACHE_FILE, 'r') as f:
            cur_cache = json.load(f)

    return


def _hash(prompt):
    prompt = [p for p in prompt if p['role'] == 'user']
    return sha256(str(prompt).encode('utf-8')).hexdigest()


def check_cache(prompt):
    hash = _hash(prompt)
    if hash in cur_cache:
        return cur_cache[hash]
    else:
        return None


def _prune_cache():
    global cur_cache
    if len(cur_cache) > MAX_CACHE_SIZE:
        diff = len(cur_cache) - MAX_CACHE_SIZE
        for k in cur_cache.keys()[:diff]:
            del cur_cache[k]
    return


def cache(prompt, response):
    hash = _hash(prompt)
    cur_cache[hash] = response
    _prune_cache()
    with open(CACHE_FILE, 'w') as f:
        json.dump(cur_cache, f)
    return


def cached(func):
    def wrapper(prompt):
        cached = check_cache(prompt.prompt)
        if cached:
            return cached
        else:
            res = func(prompt)
            cache(prompt.prompt, res)
            return res
    return wrapper
