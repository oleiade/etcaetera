import pytest

from etcaetera.adapter import Adapter


class TestAdapter:
    def test_load_is_not_implemented(self):
        adapter = Adapter()

        with pytest.raises(NotImplementedError):
            adapter.load()


