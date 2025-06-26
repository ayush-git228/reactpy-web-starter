from functools import wraps

def memo(component):
    cache = {}
    @wraps(component)
    def wrapped(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = component(*args, **kwargs)
        return cache[key]
    return wrapped
