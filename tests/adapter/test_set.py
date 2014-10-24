import pytest

from etcaetera.adapter import *


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

    def test__set_defaults_using_a_dict(self):
        s = AdapterSet(Env())
        s.defaults = {"abc": "123"}

        assert isinstance(s[0], Defaults) is True
        assert isinstance(s.defaults, Defaults) is True
        assert s.defaults.data == {"ABC": "123"}

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

    def test__set_overrides_using_a_dict(self):
        s = AdapterSet(Env())
        s.overrides = {"abc": "123"}

        assert isinstance(s[1], Overrides) is True
        assert isinstance(s.overrides, Overrides) is True
        assert s.overrides.data == {"ABC": "123"}

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

    def test_appendleft_raises_when_provided_with_non_adapter(self):
        s = AdapterSet()

        with pytest.raises(TypeError):
            s.appendleft(123)

    def test_appendleft_raises_when_providing_a_second_defaults(self):
        s = AdapterSet(Defaults())

        with pytest.raises(ValueError):
            s.appendleft(Defaults())

    def test_appendleft_raises_when_providing_a_second_overrides(self):
        s = AdapterSet(Overrides())

        with pytest.raises(ValueError):
            s.appendleft(Overrides())

    def test_appendleft_sets_defaults_property(self):
        s = AdapterSet(Env(), Env())

        assert s.defaults is None
        s.appendleft(Defaults())
        assert s.defaults is not None

    def test_appendleft_sets_defaults_overrides(self):
        s = AdapterSet(Env(), Env())

        assert s.overrides is None
        s.appendleft(Overrides())
        assert s.overrides is not None

    def test_append_raises_when_provided_with_non_adapter(self):
        s = AdapterSet()

        with pytest.raises(TypeError):
            s.append(123)

    def test_append_raises_when_providing_a_second_defaults(self):
        s = AdapterSet(Defaults())

        with pytest.raises(ValueError):
            s.append(Defaults())

    def test_append_raises_when_providing_a_second_overrides(self):
        s = AdapterSet(Overrides())

        with pytest.raises(ValueError):
            s.append(Overrides())

    def test_append_sets_defaults_property(self):
        s = AdapterSet(Env(), Env())

        assert s.defaults is None
        s.append(Defaults())
        assert s.defaults is not None

    def test_append_sets_overrides_property(self):
        s = AdapterSet(Env(), Env())

        assert s.overrides is None
        s.append(Overrides())
        assert s.overrides is not None

    def test_insert_at_negative_index_raises(self):
        s = AdapterSet()
        
        with pytest.raises(IndexError):
            s.insert(-1, Env())

    def test_insert_invalid_type_raises(self):
        s = AdapterSet()

        with pytest.raises(TypeError):
            s.insert(0, 123)

    def test_insert_a_second_defaults_at_first_index_raises(self):
        s = AdapterSet(Defaults())

        with pytest.raises(ValueError):
            s.insert(0, Defaults())

    def test_insert_a_second_overrides_at_last_index_raises(self):
        s = AdapterSet(Defaults(), Env(), Overrides())

        with pytest.raises(ValueError):
            s.insert(3, Overrides())

    def test_insert_in_the_middle(self):
        s = AdapterSet(Defaults(), Overrides())

        s.insert(1, Env())
        assert len(s) == 3
        assert isinstance(s[1], Env)

    def test_insert_at_end_with_overrides(self):
        s = AdapterSet(
            Defaults(),
            File('meh', strict=False),
            File('meh2', strict=False),
            Overrides()
        )
        s.insert(3, Env())
        assert len(s) == 5
        assert isinstance(s[3], Env)

    def test_insert_in_middle_with_overrides(self):
        s = AdapterSet(
            Defaults(),
            File('meh', strict=False),
            File('meh2', strict=False),
            Overrides()
        )
        s.insert(2, Env())
        assert len(s) == 5
        assert isinstance(s[2], Env)

    def test_insert_in_middle_without_overrides(self):
        s = AdapterSet(
            Defaults(),
            File('meh', strict=False),
            File('meh2', strict=False),
        )
        s.insert(2, Env())
        assert len(s) == 4
        assert isinstance(s[2], Env)

    def test_insert_at_end_without_overrides(self):
        s = AdapterSet(
            Defaults(),
            File('meh', strict=False),
            File('meh2', strict=False),
        )
        s.insert(3, Env())
        assert len(s) == 4
        assert isinstance(s[3], Env)

    def test_insert_at_end_without_overrides_or_defaults(self):
        s = AdapterSet(
            File('meh', strict=False),
            File('meh2', strict=False),
            File('meh3', strict=False),
        )
        s.insert(3, Env())
        assert len(s) == 4
        assert isinstance(s[3], Env)

    def test_insert_in_middle_without_overrides_or_defaults(self):
        s = AdapterSet(
            File('meh', strict=False),
            File('meh2', strict=False),
            File('meh3', strict=False),
        )
        s.insert(2, Env())
        assert len(s) == 4
        assert isinstance(s[2], Env)
