from etcaetera.adapter.base import Adapter
from etcaetera.utils import format_key


class Defaults(Adapter):
    def __init__(self, data=None, *args, **kwargs):
        super(Defaults, self).__init__(*args, **kwargs)

        if data is None:
            data = {}

        self.data = data
        self.load()

    def load(self, formatter=None):
        self.data = {self.format(k, formatter): v for k,v in self.data.items()}
