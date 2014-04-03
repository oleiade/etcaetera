from etcaetera.adapter.base import Adapter


class Defaults(Adapter):
    def __init__(self, data={}, *args, **kwargs):
        super(Defaults, self).__init__(*args, **kwargs)
        self.data = {self._format_key(k):v for k,v in data.items()}

    def load(self):
        pass
