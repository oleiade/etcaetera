try:
    from functools import reduce
except ImportError:
    pass

from etcaetera.utils import is_nested_key


class Adapter(object):
    def __init__(self, *keys, **mapping):
        self.data = {} 

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '<{} {}>'.format(self.__str__(), id(self))

    def __getitem__(self, key):
        if is_nested_key(key):
            subkeys = key.split('.')
            return reduce(lambda d, k: d[k], subkeys, self.data)

        return self.data[key]

    def __setitem__(self, key, value):
        if is_nested_key(key):
            subkeys = key.split('.')

            reduce(lambda d, k: d[k], subkeys[:-1], self.data)[subkeys[-1]] = value
            return

        self.data[key] = value

    def load(self):
        raise NotImplementedError
