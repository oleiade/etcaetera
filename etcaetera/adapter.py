import os

from etcaetera.constants import (
    JSON_EXTENSIONS,
    YAML_EXTENSIONS
)


class Adapter(object):
    def __init__(self, config=None, *args, **kwargs):
        self.data = {} 

    def _format_key(self, key):
        return key.strip().upper().replace(' ', '_')

    def load(self):
        raise NotImplementedError


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


class Argv(Adapter):
    pass


class File(Adapter):
    def __init__(self, filepath, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.filepath = filepath

    def load(self):
        _, file_extension = os.path.splitext(self.filepath)
        fd = open(self.filepath, 'r')

        if file_extension.lower() in JSON_EXTENSIONS:
            import json
            self.data = {self._format_key(k):v for k,v in json.load(fd).items()}
        elif file_extension.lower() in YAML_EXTENSIONS:
            from yaml import load as yload, dump as ydump
            try:
                from yaml import CLoader as Loader
            except ImportError:
                from yaml import Loader
            self.data = {self._format_key(k):v for k,v in yload(fd, Loader=Loader).items()}
        else:
            raise ValueError("Unhandled file extension {0}".format(file_extension))

        fd.close()


class Defaults(Adapter):
    def __init__(self, data={}, *args, **kwargs):
        super(Defaults, self).__init__(*args, **kwargs)
        self.data = {self._format_key(k):v for k,v in data.items()}

    def load(self):
        pass


class Overrides(Adapter):
    def __init__(self, data={}, *args, **kwargs):
        super(Overrides, self).__init__(*args, **kwargs)
        self.data = {self._format_key(k):v for k,v in data.items()}

    def load(self):
        pass
