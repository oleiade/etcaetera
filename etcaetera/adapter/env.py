import os

from etcaetera.adapter.base import Adapter


class Env(Adapter):
    """Environment variables adapter

    The Env adapter goal is mainly to fetch and expose
    key-value pairs from the system environment to a Config object.

    To select system environment keys provide it as an uppercased
    strings *args list. If you need to fetch a given env key as another
    end name, for example you'd wanna register USER env variable as
    MY_USER adapter key, provide your associations as a 
    {src: dest, src: dest...} **kwargs dict.
    """
    def __init__(self, *args, **kwargs):
        super(Env, self).__init__()
        self.keys = [self._format_key(k) for k in args]
        self.items = {self._format_key(k): self._format_key(v) for k, v in kwargs.items()}

    def load(self):
        env_keys = self.keys + list(self.items.keys())

        for key in [self._format_key(k) for k in env_keys]:
            env_value = os.environ.get(self._format_key(key))

            if env_value is not None:
                if key in self.items:
                    self.data[self.items[key]] = env_value
                else:
                    self.data[key] = env_value
