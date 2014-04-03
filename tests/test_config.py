import pytest
import tempfile
import json
import os

from etcaetera.config import Config
from etcaetera.adapter import (
    Adapter,
    Defaults,
    Overrides,
    File,
    Env
)


class TestConfig:
    def test_init_with_defaults_provided(self):
        defaults_adapter = Defaults({"abc": "123"})
        config = Config(defaults_adapter)
        
        assert len(config.adapters) == 1
        assert config.adapters[0] == defaults_adapter

    def test_init_with_defaults_dict_provided(self):
        defaults = {"abc": "123"}
        config = Config(defaults)

        assert len(config.adapters) == 1
        assert isinstance(config.adapters[0], Defaults) is True

    def test_init_with_invalid_type_defaults_raises(self):
        with pytest.raises(TypeError):
            config = Config(123)

    def test_adapters_setter_raises_with_invalid_type(self):
        config = Config()

        with pytest.raises(TypeError):
            config.adapters = "abc 123"

    def test_adapters_setter_raises_if_a_member_has_invalid_type(self):
        config = Config()

        with pytest.raises(TypeError):
            config.adapters = [Env(), "abc 123"]

    def test_adapters_setter_raises_if_defaults_is_not_first(self):
        defaults_adapter = Defaults({"abc": "123"})
        env_adapter = Env()
        config = Config()

        with pytest.raises(ValueError):
            # defaults_adapter should always be first
            config.adapters = [env_adapter, defaults_adapter]

    def test_adapters_setter_raises_if_overrides_is_not_last(self):
        overrides_adapter = Overrides({"abc": "123"})
        env_adapter = Env()
        config = Config()

        with pytest.raises(ValueError):
            # overrides_adapter should always be last 
            config.adapters = [overrides_adapter, env_adapter]

    def test_register_raises_with_invalid_type(self):
        config = Config()

        with pytest.raises(TypeError):
            config.register("abc 123")

    def test_register_sets_defaults_adapter_as_first_with_existing_adapters(self):
        env_adapter = Env()
        defaults_adapter = Defaults({"abc": "123"})
        config = Config()

        config.adapters = [env_adapter]
        config.register(defaults_adapter)

        assert config.adapters[0] == defaults_adapter
        assert config.adapters[1] == env_adapter

    def test_register_sets_defaults_adapter_as_first_with_empty_adapters(self):
        defaults_adapter = Defaults({"abc": "123"})
        config = Config()

        config.adapters = []
        config.register(defaults_adapter)

        assert len(config.adapters) == 1
        assert config.adapters[0] == defaults_adapter

    def test_register_a_second_defaults_overrides_existing_one(self):
        env_adapter = Env()
        defaults_adapter = Defaults({"abc": "123"})
        config = Config()
        config.adapters = [defaults_adapter, env_adapter]

        new_defaults = Defaults({"easy as": "do re mi"})
        config.register(new_defaults)
        assert config.defaults == new_defaults

    def test_register_sets_overrides_adapter_as_last_with_existing_adapters(self):
        env_adapter = Env()
        overrides_adapter = Overrides({"abc": "123"})
        config = Config()

        config.adapters = [env_adapter]
        config.register(overrides_adapter)

        assert config.adapters[0] == env_adapter
        assert config.adapters[1] == overrides_adapter 

    def test_register_sets_overrides_adapter_as_last_with_empty_adapters(self):
        overrides_adapter = Overrides({"abc": "123"})
        config = Config()

        config.adapters = []
        config.register(overrides_adapter)

        assert len(config.adapters) == 1
        assert config.adapters[0] == overrides_adapter 

    def test_register_a_second_overrides_replaces_existing_one(self):
        env_adapter = Env()
        overrides_adapter = Overrides({"abc": "123"})
        config = Config()
        config.adapters = [env_adapter, overrides_adapter]

        new_overrides = Overrides({"easy as": "do re mi"})
        config.register(new_overrides)
        assert config.overrides == new_overrides

    def test_register_a_non_special_adapter_with_empty_adapters(self):
        env_adapter = Env()
        config = Config()

        config.register(env_adapter)
        
        assert len(config.adapters) == 1
        assert config.adapters[0] == env_adapter

    def test_register_non_special_adapters_protects_order(self):
        env_adapter = Env()
        file_adapter = File('/tmp/test')
        config = Config()

        config.register(env_adapter)
        config.register(file_adapter)
        
        assert len(config.adapters) == 2
        assert config.adapters[0] == env_adapter
        assert config.adapters[1] == file_adapter

    def test_register_non_special_adapters_with_overrides(self):
        env_adapter = Env()
        file_adapter = File('/tmp/test')
        overrides_adapter = Overrides()

        config = Config()
        config.adapters = [overrides_adapter]

        config.register(env_adapter)
        config.register(file_adapter)

        assert len(config.adapters) == 3
        assert config.adapters[0] == env_adapter
        assert config.adapters[1] == file_adapter
        assert config.adapters[2] == overrides_adapter

    def test_register_multiple_adapters(self):
        config = Config()
        defaults_adapter = Defaults()
        env_adapter = Env()
        file_adapter = File('/tmp/test')
        config.register(defaults_adapter, env_adapter, file_adapter)

        assert len(config.adapters) == 3
        assert config.adapters[0] == defaults_adapter
        assert config.adapters[1] == env_adapter
        assert config.adapters[2] == file_adapter

    def test_add_subconfig_adds_config_as_attribute(self):
        main_config = Config()
        sub_config = Config({"abc": "123"})

        main_config.add_subconfig('mysubconfig', sub_config)
        assert 'mysubconfig' in main_config._subconfigs
        assert main_config._subconfigs['mysubconfig'] == sub_config

        assert hasattr(main_config, 'mysubconfig')
        assert main_config.mysubconfig == sub_config

    def test_add_subconfig_with_invalid_type_raises(self):
        config = Config()

        with pytest.raises(TypeError):
            config.add_subconfig(config)

    def test_load_method_loads_values_from_adapters(self):
        defaults = Defaults({"abc": "123"})
        config = Config()

        config.register(defaults)
        config.load()

        assert "ABC" in config
        assert config["ABC"] == "123"

    def test_load_method_forces_subconfig_adapters_loading(self):
        main_config = Config()

        subconfig = Config()
        subconfig_env_adapter = Env("TEST")
        subconfig.register(subconfig_env_adapter)

        main_config.add_subconfig('test_subconfig', subconfig)

        os.environ["TEST"] = "test"

        assert hasattr(main_config, 'test_subconfig')
        assert main_config.test_subconfig == subconfig
        assert not main_config.test_subconfig

        main_config.load()

        assert 'TEST' in main_config.test_subconfig
        assert main_config.test_subconfig['TEST'] == 'test'

        del os.environ["TEST"]
        

    def test_load_passes_its_keys_to_env_loading(self):
        env = Env("USER", "PATH")
        config = Config({"PATH":None})

        config.register(env)
        config.load()

        assert "USER" in config
        assert "PATH" in config
        assert config["USER"] == os.environ["USER"]
        assert config["PATH"] == os.environ["PATH"]

