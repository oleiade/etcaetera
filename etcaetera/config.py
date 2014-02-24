from etcaetera.policy import Policy
from etcaetera.adapter import (
    Adapter,
    Defaults
)


class Config(dict):
    def __init__(self, defaults=None, adapters=[]):
        self.adapters = adapters

        if defaults is not None:
            self.defaults = defaults
            self.defaults.load()

    def register(self, adapter):
        """Registers an adapter to be applied by config"""
        pass

    def unregister(self, adapter):
        """Unregisters an adapter from the config"""
        pass

    @property
    def adapters(self):
        if not hasattr(self, '_adapters'):
            self._adapters = set()
        return self._adapters

    @adapters.setter
    def adapters(self, value):
        # Ensure adapters is a suitable sequence
        if not isinstance(value, (list, tuple)):
            raise TypeError(
                "Adapters value has to be whether a list or a tuple. "
                "Got {0} provided.".format(type(value))
            )
        elif isinstance(value, tuple):
            value = list(value)

        if any(not isinstance(p, Adapter) for p in value):
            raise ValueError("Every member of adapters value has to be of type Adapter")

        self._adapters = value

    @property
    def defaults(self):
        if not hasattr(self, '_defaults'):
            self._defaults = Defaults()
        return self._defaults

    @defaults.setter
    def defaults(self, value):
        if not isinstance(value, (Defaults, dict)):
            raise TypeError(
                "Defaults value has to be of Defaults or dict type. "

                "Got {0} instead.".format(type(value))
            )

        if isinstance(value, dict):
            self._defaults = Defaults(config=self, data=value)
        else:
            self._defaults = value

    def load(self):
        for adapter in self.adapters:
            adapter.load()
