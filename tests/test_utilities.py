"""
Test of core.utilities.check_types

"""
import unittest

from annotation_validation.core.utilities import check_types


class MyTestCase(unittest.TestCase):

    def my_assert(self, exp1, exp2):
        self.assertEqual(
            exp1, exp2, "<< {} >> != << {} >>".format(exp1, exp2))
    
    def test_1(self):
        @check_types
        def test_func(a:int, b:str, c:int=5, d=1):
            pass

        test_func(1, '2')

    def test_test_args_2(self):
        @check_types
        def test_func(a:int, b:str, c=5, e=3, d=1):
            pass

        test_func(*[1, '2'], **{'e': 8})
      

    def test_test_args_3(self):
        @check_types
        def test_func(a:int, b:str, c=5, e=3, d=1, *args):
            pass

        test_func(*[1, '2'], **{'e': 8})
 
    def test_test_args_4(self):
        @check_types
        def test_func(a:int, b:str, c=5, e=3, d=1, *args, **kwargs):
            pass
        
        test_func(*[1, '2'], **{'e': 8})

    def test_test_args_5(self):
        @check_types
        def test_func(a:int, b:str, c=5, *args, e=3, d=1, **kwargs):
            pass

        test_func(*[1, '2'], **{'e': 8})

    def test_test_args_6(self):
        @check_types
        def test_func(a:int, b:str, c=5, *args, e=3, d=1, **kwargs):
            pass

        with self.assertRaises(TypeError):
            test_func(*[1, 2], **{'e': 8})


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result_test = runner.run(suite)
