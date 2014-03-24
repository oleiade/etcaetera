class Adapter(object):
    def __init__(self, config=None, *args, **kwargs):
        self.data = {} 

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '<{} {}>'.format(self.__str__(), id(self))

    def _format_key(self, key):
        return key.strip().upper().replace(' ', '_')

    def load(self):
        raise NotImplementedError
