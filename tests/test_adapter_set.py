import pytest

from etcaetera.adapter import *
from etcaetera.adapter_set import AdapterSet


class TestAdapterSet:
    def test_set_defaults_to_invalid_type_raises(self):
        s = AdapterSet()

        with pytest.raises(TypeError):
            s.defaults = 123

    def test_set_overrides_to_invalid_type_raises(self):
        s = AdapterSet()
        
        with pytest.raises(TypeError):
            s.defaults = "123"

    def test_setitem_using_a_defaults_pointing_other_than_first_index_raises(self):
        s = AdapterSet(Env(), Overrides())

        with pytest.raises(IndexError):
            s[1] = Defaults()

    def test_setitem_using_an_overrides_pointing_other_than_last_index_raises(self):
        s = AdapterSet(Defaults(), Env())

        with pytest.raises(IndexError):
            s[0] = Overrides()

    def test__set_defaults_with_invalid_type_raises(self):
        s = AdapterSet()

        with pytest.raises(TypeError):
            s.defaults = 123

    def test__set_defaults_of_empty_adapters_set(self):
        s = AdapterSet()
        s.defaults = Defaults()

        assert isinstance(s[0], Defaults) is True

    def test__set_defaults_of_non_empty_adapters_set_puts_it_first(self):
        s = AdapterSet(Env())
        s.defaults = Defaults()

        assert isinstance(s[0], Defaults) is True

    def test__set_overrides_with_invalid_type_raises(self):
        s = AdapterSet()

        with pytest.raises(TypeError):
            s.overrides = 123

    def test__set_overrides_of_empty_adapters_set(self):
        s = AdapterSet()
        s.overrides = Overrides()

        assert isinstance(s[0], Overrides) is True

    def test__set_overrides_of_non_empty_adapters_set_puts_it_last(self):
        s = AdapterSet(Env())
        s.overrides = Overrides()

        assert isinstance(s[1], Overrides) is True

    def test_init_with_invalid_adapters_raises(self):
        with pytest.raises(TypeError):
            AdapterSet(123, "abc")

    def test_init_with_defaults_not_being_first_raises(self):
        defaults_adapter = Defaults({"abc": "123"})
        env_adapter = Env()

        with pytest.raises(ValueError):
            AdapterSet(env_adapter, defaults_adapter)

    def test_init_with_multiple_defaults_raises(self):
        defaults_adapter = Defaults({"abc": "123"})

        with pytest.raises(ValueError):
            AdapterSet(defaults_adapter, defaults_adapter)

    def test_init_with_overrides_not_being_last_raises(self):
        overrides_adapter = Overrides({"abc": "123"})
        env_adapter = Env()

        with pytest.raises(ValueError):
            AdapterSet(overrides_adapter, env_adapter)

    def test_init_with_multiple_overrides_raises(self):
        overrides_adapter = Overrides({"abc": "123"})

        with pytest.raises(ValueError):
            AdapterSet(overrides_adapter, overrides_adapter)

    def test_init_adapters_order_is_protected(self):
        first_env_adapter = Env()
        second_env_adapter = Env()
        defaults_adapter = Defaults()
        overrides_adapter = Overrides()

        s = AdapterSet(
            defaults_adapter,
            first_env_adapter,
            second_env_adapter,
            overrides_adapter
        )

        assert len(s) == 4
        assert isinstance(s[0], Defaults) and s[0] == defaults_adapter
        assert isinstance(s[1], Env) and s[1] == first_env_adapter
        assert isinstance(s[2], Env) and s[2] == second_env_adapter
        assert isinstance(s[3], Overrides) and s[3] == overrides_adapter
