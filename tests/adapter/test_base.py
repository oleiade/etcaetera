import pytest

from etcaetera.adapter import Adapter


class TestAdapter:
    def test__format_env_key_with_mixed_case(self):
        adapter = Adapter()
        assert adapter._format_key('abC 123') == 'ABC_123'

    def test__format_env_key_with_lower_case(self):
        adapter = Adapter()
        assert adapter._format_key('abc 123') == 'ABC_123'

    def test__format_env_key_with_upper_case(self):
        adapter = Adapter()
        assert adapter._format_key('ABC 123') == 'ABC_123'

    def test__format_env_key_with_trailing_spaces(self):
        adapter = Adapter()
        assert adapter._format_key('   abc 123  ') == 'ABC_123'

    def test_load_is_not_implemented(self):
        adapter = Adapter()

        with pytest.raises(NotImplementedError):
            adapter.load()


