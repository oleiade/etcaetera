import os

from etcaetera.constants import (
    JSON_EXTENSIONS,
    YAML_EXTENSIONS
)


class Adapter(object):
    def __init__(self, *args, **kwargs):
        self.data = {} 

    def load(self):
        raise NotImplementedError


class Env(Adapter):
    def __init__(self, keys=[], *args, **kwargs):
        super(Env, self).__init__(*args, **kwargs)
        self.keys = keys

    def _format_env_key(self, key):
        return key.strip().upper().replace(' ', '_')

    def load(self):
        keys = self.keys

        for key in keys:
            env_value = os.environ.get(self._format_env_key(key))
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
            self.data = json.load(fd)
        elif file_extension.lower() in YAML_EXTENSIONS:
            import yaml
            self.data = yaml.load(fd, Loader=yaml.CLoader)
        else:
            raise ValueError("Unhandled file extension {0}".format(file_extension))

        fd.close()


class Defaults(Adapter):
    def __init__(self, config, data={}, *args, **kwargs):
        super(Defaults, self).__init__(*args, **kwargs)
        self.data = data

    def load(self):
        pass
        

