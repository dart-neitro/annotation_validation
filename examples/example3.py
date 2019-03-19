"""
Example custom class using @check_types
"""
from annotation_validation import check_types, AnnotationTypeError


class MyClass:
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        return self.n == other.n


@check_types
def func(a: MyClass):
    return a


try:
    z = list()
    z.append(func(MyClass(1)))
    z.append(func(MyClass(2)))
    func('c')
except AnnotationTypeError:
    pass
except Exception as e:
    raise e


assert z == [MyClass(1), MyClass(2)]
