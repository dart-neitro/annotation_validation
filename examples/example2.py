"""
multi type
"""
from annotation_validation import check_types, AnnotationTypeError


@check_types
def func(a: (str, int)):
    return a


try:
    z = list()
    z.append(func(1))
    z.append(func(2))
    func('c')
except AnnotationTypeError:
    pass
except Exception as e:
    raise e


assert z == [1, 2, 'c']
