"""
Test of core.Parser

"""
import unittest

from annotation_validation.core.parser import Parser

from annotation_validation.core.exceptions import (
    AnnotationTypeError, ReturnAnnotationTypeError)


class MyTestCase(unittest.TestCase):

    def my_assert(self, exp1, exp2):
        self.assertEqual(
            exp1, exp2, "<< {} >> != << {} >>".format(exp1, exp2))

    def test_get_arguments(self):
        def test_func(a, b, c, d):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c', 'd'), (), (), ()))

    def test_get_arguments_2(self):
        def test_func(a, b, c, d, *args):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c', 'd'), (), ('args',),  ()))

    def test_get_arguments_3(self):
        def test_func(a, b, c, d, e, *args, **kwargs):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c', 'd', 'e'), (), ('args',), ('kwargs',)))

    def test_get_arguments_4(self):
        def test_func(a, b, c=4, *args, d, e, **kwargs):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c'), ('d', 'e'), ('args',), ('kwargs',)))

    def test_get_arguments_5(self):
        """
        Test tab

        :return:
        """
        def test_func(a,
                      b,
                      c=4, *args, d, e, **kwargs):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c'), ('d', 'e'), ('args',), ('kwargs',)))


    def test_required_args_1(self):
        def test_func(a, b, c=5, d=1):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.required_args()),
            ('a', 'b'))

    def test_required_args_2(self):
        def test_func(a, b, c, d, *args):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.required_args()),
            ('a', 'b', 'c', 'd'))

    def test_required_args_3(self):
        def test_func(a, b, c, d, e, *args, **kwargs):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.required_args()),
            ('a', 'b', 'c', 'd', 'e'))

    def test_required_args_4(self):
        def test_func(a, b, c=4, *args, d, e, **kwargs):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.required_args()),
            ('a', 'b', 'd', 'e'))

    def test_check_args_1(self):
        def test_func(a:int, b:str, c:int=5, d=1):
            pass

        parser = Parser(test_func)
        self.my_assert(
            parser.check_args(1, '2'),
            True
            )

    def test_check_args_2(self):
        def test_func(a:int, b:str, c=5, e=3, d=1):
            pass

        parser = Parser(test_func)

        self.my_assert(
            parser.check_args(*[1, '2'], **{'e': 8}),
            True
            )

    def test_check_args_3(self):
        def test_func(a:int, b:str, c=5, e=3, d=1, *args):
            pass

        parser = Parser(test_func)

        self.my_assert(
            parser.check_args(*[1, '2'], **{'e': 8}),
            True
            )

    def test_check_args_4(self):
        def test_func(a:int, b:str, c=5, e=3, d=1, *args, **kwargs):
            pass

        parser = Parser(test_func)

        self.my_assert(
            parser.check_args(*[1, '2'], **{'e': 8}),
            True
            )

    def test_check_args_5(self):
        def test_func(a:int, b:str, c=5, *args, e=3, d=1, **kwargs):
            pass

        parser = Parser(test_func)

        self.my_assert(
            parser.check_args(*[1, '2'], **{'e': 8}),
            True
            )

    def test_check_args_6(self):
        def test_func(a:int):
            pass

        parser = Parser(test_func)

        with self.assertRaises(AnnotationTypeError):
            parser.check_args('a')

    def test_check_return_1(self):
        def test_func() -> int:
            pass

        parser = Parser(test_func)

        with self.assertRaises(ReturnAnnotationTypeError):
            parser.check_return('a')

    def test_check_return_2(self):
        def test_func() -> int:
            pass

        parser = Parser(test_func)

        with self.assertRaises(ReturnAnnotationTypeError):
            parser.check_return(object)

    def test_check_return_3(self):
        def test_func() -> int:
            pass

        parser = Parser(test_func)

        with self.assertRaises(ReturnAnnotationTypeError):
            parser.check_return(None)

    def test_check_return_4(self):
        def test_func() -> int:
            pass

        parser = Parser(test_func)

        parser.check_return(True)
        parser.check_return(False)
        parser.check_return(1)

    def test_check_return_5(self):
        def test_func() -> tuple:
            pass

        parser = Parser(test_func)

        parser.check_return(tuple([1, 2, 3]))

    def test_check_return_6(self):
        def test_func() -> (tuple, list):
            pass

        parser = Parser(test_func)

        parser.check_return(tuple([1, 2, 3]))
        parser.check_return([1, 2, 3])

    def test_check_return_7(self):
        def test_func():
            pass

        parser = Parser(test_func)

        parser.check_return(True)
        parser.check_return(False)
        parser.check_return(1)
        parser.check_return('1')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result_test = runner.run(suite)
