from collections import deque

from etcaetera.adapter import (
    Adapter,
    AdapterSet,
    Defaults,
    Overrides,
    Env
)


class Config(dict):
    def __init__(self, defaults=None, overrides=None, *adapters):
        self.adapters = AdapterSet(*adapters)

        if defaults is not None:
            self.defaults = defaults

        if overrides is not None:
            self.overrides = overrides

    def register(self, *adapters):
        """Registers an adapter to be applied by config"""
        for adapter in adapters:
            if isinstance(adapter, Defaults):
                self.adapters.defaults = adapter
            elif isinstance(adapter, Overrides):
                self.adapters.overrides = adapter
            else:
                if self.adapters.overrides is not None:
                    # If adapters contains an Overrides adapter,
                    # insert at the index before it.
                    self.adapters.insert(len(self.adapters) - 1, adapter)
                else:
                    # Otherwise, append it
                    self.adapters.append(adapter)

    @property
    def defaults(self):
        return self.adapters.defaults

    @defaults.setter
    def defaults(self, value):
        self.adapters.defaults = value

    @property
    def overrides(self):
        return self.adapters.overrides

    @overrides.setter
    def overrides(self, value):
        self.adapters.overrides = value

    @property
    def adapters(self):
        if not hasattr(self, '_adapters'):
            self._adapters = AdapterSet()
        return self._adapters

    @adapters.setter
    def adapters(self, value):
        # Ensure adapters is a list of adapters
        if not isinstance(value, (list, AdapterSet)):
            raise TypeError("adapters value has to be a list or AdapterSet.")

        self._adapters = AdapterSet(*value)

    def load(self):
        for adapter in self.adapters:
            if isinstance(adapter, Env):
                adapter.load(keys=self.keys())
            else:
                adapter.load()

            self.update(adapter.data)
