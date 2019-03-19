"""
Test of @check_types

"""
import unittest

from annotation_validation.core.utilities import check_types
from annotation_validation.core.exceptions import (
    AnnotationTypeError, ReturnAnnotationTypeError)


class MyTestCase(unittest.TestCase):
    
    def test_check_types_1(self):
        @check_types
        def test_func(a:int, b:str, c:int=5, d=1):
            pass

        test_func(1, '2')

    def test_check_types_2(self):
        @check_types
        def test_func(a:int, b:str, c=5, e=3, d=1):
            pass

        test_func(*[1, '2'], **{'e': 8})

    def test_check_types_3(self):
        @check_types
        def test_func(a:int, b:str, c=5, e=3, d=1, *args):
            pass

        test_func(*[1, '2'], **{'e': 8})
 
    def test_check_types_4(self):
        @check_types
        def test_func(a:int, b:str, c=5, e=3, d=1, *args, **kwargs):
            pass
        
        test_func(*[1, '2'], **{'e': 8})

    def test_check_types_5(self):
        @check_types
        def test_func(a:int, b:str, c=5, *args, e=3, d=1, **kwargs):
            pass

        test_func(*[1, '2'], **{'e': 8})

    def test_check_types_6(self):
        @check_types
        def test_func(a:int, b:str, c=5, *args, e=3, d=1, **kwargs):
            pass

        with self.assertRaises(AnnotationTypeError):
            test_func(*[1, 2], **{'e': 8})

    def test_check_types_7(self):
        @check_types
        def test_func() -> str:
            return 1

        with self.assertRaises(ReturnAnnotationTypeError):
            test_func()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result_test = runner.run(suite)
