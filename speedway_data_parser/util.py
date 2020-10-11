import logging
from functools import wraps

log = logging.getLogger(__name__)

def catch_exceptions(lst_exceptions):
    if not isinstance(lst_exceptions, tuple):
        _lst_exceptions = (lst_exceptions,)
    else:
        _lst_exceptions = lst_exceptions

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                ret = f(*args, **kwargs)
                return ret
            except _lst_exceptions:
                log.error(u'Przechwycono błąd w funkcji %s')
        return wrapper
    return decorator
