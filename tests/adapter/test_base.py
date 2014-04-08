import pytest

from etcaetera.adapter import Adapter
from etcaetera.exceptions import MalformationError


class TestAdapter:
    def test___getitem___with_existing_nested_key_returns_its_value(self):
        adapter = Adapter()
        adapter.data['abc'] = {}
        adapter.data['abc']['123'] = 'easy as'

        assert adapter['abc.123'] == adapter['abc']['123']

    def test___getitem___with_flat_existing_key_returns_its_value(self):
        adapter = Adapter()
        adapter.data['abc'] = 'easy as'

        assert adapter['abc'] == 'easy as'

    def test___getitem___with_invalid_nested_key_raises(self):
        adapter = Adapter()
        adapter.data['abc'] = {}
        adapter.data['abc']['123'] = 'easy as'

        with pytest.raises(MalformationError):
            adapter['..abc']

    def test___setitem___with_existing_nested_key_sets_its_value(self):
        adapter = Adapter()
        adapter.data['abc'] = {}

        adapter['abc.123'] = 'easy as'

        assert adapter.data['abc']['123'] == 'easy as'

    def test___setitem___with_flat_existing_key_sets_its_value(self):
        adapter = Adapter()
        adapter['abc'] = 'easy as'

        assert adapter['abc'] == 'easy as'

    def test___setitem___with_invalid_nested_key_raises(self):
        adapter = Adapter()

        with pytest.raises(MalformationError):
            adapter['..abc'] = 'easy as'
        
    def test_load_is_not_implemented(self):
        adapter = Adapter()

        with pytest.raises(NotImplementedError):
            adapter.load()


