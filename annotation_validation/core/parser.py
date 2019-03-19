"""
Parser arguments
"""
from inspect import signature

from annotation_validation.core.exceptions import (
    AnnotationTypeError, ReturnAnnotationTypeError)


class Parser:
    """
    Parsing arguments and argument's annotations of the function and
    checking it
    """
    func = None

    def __init__(self, func):
        self.func = func

    @property
    def var_names_from_sig(self):
        """
        Parsing function's argument from function's signature
        :return:
        """

        result = []
        sig = signature(self.func)

        str_sig = str(sig)
        str_sig = str_sig[str_sig.find('(') + 1:str_sig.rfind(')')]

        if not len(sig._parameters) and not str_sig:
            return []

        if len(sig._parameters) != len(str_sig.split(',')):
            raise Exception('Oooops!')

        for arg in str(sig)[1:-1].split(','):
            result.append(arg.split('=')[0].split(':')[0].strip())

        clear_result = [x for x in result if not x.startswith('*')]

        clear_result += [
            x for x in result if x.startswith('*') and x.count('*') == 1]
        clear_result += [
            x for x in result if x.startswith('*') and x.count('*') == 2]

        return clear_result

    def get_arguments(self):
        """
        Parsing function's argument and group:
        (arguments),
        (keyword arguments),
        (addition arguments like *args),
        (addition keyword arguments like **kwargs)

        :return:
        """

        var_names = self.func.__code__.co_varnames
        var_names_from_sig = list(self.var_names_from_sig)
        var_names = var_names[:len(var_names_from_sig)]

        # args
        position = self.func.__code__.co_argcount
        attr_names = tuple(var_names[:position])

        var_names = var_names[position:]
        var_names_from_sig = var_names_from_sig[position:]
        yield attr_names

        # kwargs
        if self.func.__code__.co_kwonlyargcount:
            position = self.func.__code__.co_kwonlyargcount
            attr_names = tuple(var_names[:position])

            var_names = var_names[position:]
            var_names_from_sig = var_names_from_sig[position:]
            yield attr_names
        else:
            yield ()

        # *args
        if var_names_from_sig and var_names_from_sig[0].count('*') == 1:
            attr_names = (var_names[0], )
            var_names = var_names[1:]
            var_names_from_sig = var_names_from_sig[1:]
            yield attr_names
        else:
            yield ()

        if var_names_from_sig and var_names_from_sig[0].count('*') == 2:
            attr_names = (var_names[0], )
            yield attr_names
        else:
            yield ()

        return

    def required_args(self):
        var_names = list(self.get_arguments())
        var_names = list(var_names[0]) + list(var_names[1])
        var_defaults = self.get_default_value_from_sig()
        return [x for x in var_names if x not in var_defaults]

    def get_default_value_from_sig(self):

        sig = signature(self.func)

        var_names = [
            n for n, p in sig.parameters.items() if p._default != p.empty]
        if var_names:
            return dict(zip(var_names, self.func.__defaults__))

        return dict()

    def route_parameters(self, *args, **kwargs):
        """
        Transform *args & **kwargs to function's format

        :param args:
        :param kwargs:

        :return:
        """
        var_names = list(self.get_arguments())
        dict(zip(var_names, args[:len(var_names[0])]))

    def check_args(self, *args, **kwargs):
        var_names = list(self.get_arguments())
        var_types = self.func.__annotations__

        var_args = dict(zip(var_names[0], args[:len(var_names[0])]))

        # args
        for var_name in var_args:
            if var_name in var_types:
                if not isinstance(var_args[var_name], var_types[var_name]):
                    raise AnnotationTypeError(
                        'The parameter <{var_name}> '
                        'must be {type_name}, not {type_current}'.format(
                            var_name=var_name,
                            type_name=str(var_types[var_name]),
                            type_current=str(type(var_args[var_name]))
                        ))

        # kwargs
        for var_name in kwargs:
            if var_name in var_types:
                if not isinstance(kwargs[var_name], var_types[var_name]):
                    raise AnnotationTypeError(
                        'The parameter <{var_name}> '
                        'must be {type_name}, not {type_current}'.format(
                            var_name=var_name,
                            type_name=str(var_types[var_name]),
                            type_current=str(type(kwargs[var_name]))
                        ))

        return True

    def test_return(self, return_value):
        """
        test return value
        :return:
        """
        var_types = self.func.__annotations__
        if 'return' in var_types:
            if not isinstance(return_value, var_types['return']):
                raise ReturnAnnotationTypeError(
                    'The return value '
                    'must be {type_name}, not {type_current}'.format(
                        type_name=str(var_types['return']),
                        type_current=str(type(return_value))
                        )
                    )
        return True
