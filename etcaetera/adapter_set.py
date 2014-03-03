from collections import deque

from etcaetera.adapter import *


class AdapterSet(deque):
    def __init__(self, *adapters):
        super(AdapterSet, self).__init__()
        self._adapters = self._load_adapters(adapters)

    def __setitem__(self, key, value):
        if isinstance(value, Defaults) and key != 0:
                raise IndexError("Defaults adapter shall always be unique and first")  
        elif isinstance(value, Overrides) and key != (len(self) - 1):
                raise IndexError("Overrides adapter shall always be unique and last")

        super(AdapterSet, self).__setitem__(key, value)

    @property
    def defaults(self):
        if not hasattr(self, '_defaults'):
            self._defaults = None
        return self._defaults

    @defaults.setter
    def defaults(self, value):
        if not isinstance(value, Defaults):
            raise TypeError("Attribute must be of Defaults type")
        self._defaults = value

    @property
    def overrides(self):
        if not hasattr(self, '_overrides'):
            self._overrides = None
        return self._overrides

    @overrides.setter
    def overrides(self, value):
        if not isinstance(value, Overrides):
            raise TypeError("Attribute must be of Overrides type")
        self._overrides = value

    def _load_adapters(self, adapters):
        adapters_collection = []

        for index, adapter in enumerate(adapters):
            if (isinstance(adapter, Defaults) and
                (self.defaults is not None or index != 0)):
                raise ValueError("Cannot add two defaults adapter to the same set")
            elif (isinstance(adapter, Overrides) and
                  (self.overrides is not None or index < (len(adapters) - 1))):
                raise ValueError("Cannot add two overrides adapters to the same set")
            elif not isinstance(adapter, Adapter):
                raise TypeError("AdapterSet can only contain Adapter type objects")

            super(AdapterSet, self).append(adapter)
