"""
Decorator for check types
"""
from functools import wraps

from annotation_validation.core.parser import Parser


def check_types(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        parser = Parser(f)
        parser.check_args(*args, **kwargs)
        result = f(*args, **kwargs)
        parser.test_return(result)
        return result
    return wrapper
