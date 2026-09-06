import inspect
from functools import wraps
from typing import Callable

from cachetools import TTLCache

DEFAULT_EXCLUDED_PARAMS = frozenset({"db"})

_all_caches: list[TTLCache] = []


def clear_all_caches() -> None:
    """Clear every cache created by @cached. Intended for test isolation between requests."""
    for store in _all_caches:
        store.clear()


def cached(ttl: float, maxsize: int = 256, exclude: frozenset[str] = DEFAULT_EXCLUDED_PARAMS):
    """Cache an async endpoint's return value in-process, keyed on its call arguments.

    Excludes params like the DB session (not hashable/meaningful for a cache key) from the key.
    Each decorated function gets its own TTLCache, created once at import time.
    """

    def decorator(func: Callable):
        store: TTLCache = TTLCache(maxsize=maxsize, ttl=ttl)
        _all_caches.append(store)
        signature = inspect.signature(func)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            key = tuple(
                (name, value)
                for name, value in sorted(bound.arguments.items())
                if name not in exclude
            )

            if key in store:
                return store[key]

            result = await func(*args, **kwargs)
            store[key] = result
            return result

        return wrapper

    return decorator
