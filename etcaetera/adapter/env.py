import os

from etcaetera.adapter.base import Adapter


class Env(Adapter):
    """Environment variables adapter

    Loads values from the system environment.
    Keys to be fetched should be passed a string list.
    """
    def __init__(self, keys=[], *args, **kwargs):
        super(Env, self).__init__(*args, **kwargs)
        self.keys = [self._format_key(k) for k in keys]

    def load(self, keys=None):
        env_keys = self.keys

        if keys is not None and isinstance(keys, list):
            env_keys.extend(keys)

        for key in [self._format_key(k) for k in env_keys]:
            env_value = os.environ.get(self._format_key(key))
            if env_value is not None:
                self.data[key] = env_value
