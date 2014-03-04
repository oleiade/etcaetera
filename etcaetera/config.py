from collections import deque

from etcaetera.adapter import (
    Adapter,
    AdapterSet,
    Defaults,
    Overrides,
    Env
)


class Config(dict):
    def __init__(self, defaults=None, *adapters):
        self.adapters = AdapterSet(*adapters)

        if defaults is not None:
            if not isinstance(defaults, (Defaults, dict)):
                raise TypeError("defaults has to be of Defaults type")

            if isinstance(defaults, dict):
                self.register(Defaults(data=defaults))
            else:
                self.register(defaults)

    def register(self, adapter):
        """Registers an adapter to be applied by config"""
        if not isinstance(adapter, Adapter):
            raise TypeError("adapter has to be of Adapter type.")

        has_defaults = len(self.adapters) >= 1 and isinstance(self.adapters[0], Defaults)
        has_overrides = len(self.adapters) >= 1 and isinstance(self.adapters[len(self.adapters) - 1], Overrides)

        if isinstance(adapter, Defaults):
            if has_defaults is True:
                raise ValueError("Config can have only one Defaults adapter")
            self.adapters.appendleft(adapter)
        elif isinstance(adapter, Overrides):
            if has_overrides is True:
                raise ValueError("Config can have only one Overrides adapter")
            self.adapters.append(adapter)
        else:
            if has_overrides is True:
                # If adapters contains an Overrides adapter,
                # insert at the index before it.
                self.adapters.rotate(1)
                self.adapters.append(adapter)
                self.adapters.rotate(-1)
                # self.adapters.insert(len(self.adapters) - 1, adapter)
            else:
                # Otherwise, append it
                self.adapters.append(adapter)

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

        # Ensure Defaults are unique and first adapter, and
        # Overrides are unique and last
        for idx, adapter in enumerate(value):
            if not isinstance(adapter, Adapter):
                raise TypeError("adapters value have to be of Adapter type.")
            elif isinstance(adapter, Defaults) and idx != 0:
                raise ValueError("Defaults adapter should always be first.")
            elif isinstance(adapter, Overrides) and idx != (len(value) - 1):
                raise ValueError("Overrides adapter should always be last.")

        self._adapters = AdapterSet(*value)

    def load(self):
        for adapter in self.adapters:
            if isinstance(adapter, Env):
                adapter.load(keys=self.keys())
            else:
                adapter.load()

            self.update(adapter.data)
