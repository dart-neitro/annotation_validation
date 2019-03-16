from functools import wraps
from inspect import signature


class Parser:
    func = None

    def __init__(self, func):
        self.func = func

    @property
    def var_names(self):
        return self.func.__code__.co_varnames

    @property
    def var_names_from_sig(self):
        result = []
        sig = signature(self.func)

        if len(sig._parameters) != len(str(sig)[1:-1].split(',')):
            raise Exception('Oooops! ')

        for arg in str(sig)[1:-1].split(','):
            result.append(arg.split('=')[0].split(':')[0].strip())

        clear_result = [x for x in result if not x.startswith('*')]

        clear_result += [
            x for x in result if x.startswith('*') and x.count('*') == 1]
        clear_result += [
            x for x in result if x.startswith('*') and x.count('*') == 2]

        return clear_result

    def get_arguments(self):

        var_names = self.func.__code__.co_varnames
        var_names_from_sig = list(self.var_names_from_sig)
        var_names = var_names[:len(var_names_from_sig)]

        # args
        position = self.func.__code__.co_argcount
        attrs = tuple(var_names[:position])

        var_names = var_names[position:]
        var_names_from_sig = var_names_from_sig[position:]
        yield attrs

        # kwargs
        if self.func.__code__.co_kwonlyargcount:
            position = self.func.__code__.co_kwonlyargcount
            attrs = tuple(var_names[:position])

            var_names = var_names[position:]
            var_names_from_sig = var_names_from_sig[position:]
            yield attrs
        else:
            yield ()

        # *args
        if var_names_from_sig and var_names_from_sig[0].count('*') == 1:
            attrs = (var_names[0], )
            var_names = var_names[1:]
            var_names_from_sig = var_names_from_sig[1:]
            yield attrs
        else:
            yield ()

        if var_names_from_sig and var_names_from_sig[0].count('*') == 2:
            attrs = (var_names[0], )
            yield attrs
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

