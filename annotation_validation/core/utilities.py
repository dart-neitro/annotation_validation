"""
decorator
"""
from functools import wraps

from annotation_validation.core.parser import Parser


def check_types(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        parser = Parser(f)
        parser.test_args(*args, **kwargs)
        return f(*args, **kwargs)
    return wrapper
