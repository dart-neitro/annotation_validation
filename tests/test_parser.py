import unittest

from core.parser import Parser


class MyTestCase(unittest.TestCase):

    def my_assert(self, exp1, exp2):
        self.assertEqual(
            exp1, exp2, "<< {} >> != << {} >>".format(exp1, exp2))

    def test_1(self):
        def test_func(a, b, c, d):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c', 'd'), (), (), ()))

    def test_2(self):
        def test_func(a, b, c, d, *args):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c', 'd'), (), ('args',),  ()))

    def test_3(self):
        def test_func(a, b, c, d, e, *args, **kwargs):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c', 'd', 'e'), (), ('args',), ('kwargs',)))

    def test_4(self):
        def test_func(a, b, c=4, *args, d, e, **kwargs):
            pass

        parser = Parser(test_func)
        self.my_assert(
            tuple(parser.get_arguments()),
            (('a', 'b', 'c'), ('d', 'e'), ('args',), ('kwargs',)))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result_test = runner.run(suite)
