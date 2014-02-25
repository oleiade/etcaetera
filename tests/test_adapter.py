import pytest
import os
import tempfile
import json
import yaml

from etcaetera.config import Config
from etcaetera.adapter import (
    Adapter,
    Env,
    File,
    Module,
    Defaults
)


@pytest.fixture(scope="module")
def json_file():
    test_data = {'abc': '123'}
    sample_json_file = tempfile.NamedTemporaryFile(
        suffix='.json',
        dir='/tmp',
        delete=False
    )
    dumped_data = json.dumps(test_data)
    sample_json_file.write(dumped_data.encode('utf-8'))  # Py3 compatibility
    sample_json_file.close()

    def fin():
        os.remove(sample_json_file.name)

    return sample_json_file


@pytest.fixture(scope="module")
def yaml_file():
    test_data = {'abc': '123'}
    sample_yaml_file = tempfile.NamedTemporaryFile(
        suffix='.yaml',
        dir='/tmp',
        delete=False
    )
    dumped_data = yaml.dump(test_data)
    sample_yaml_file.write(dumped_data.encode('utf-8'))  # Py3 compatibility
    sample_yaml_file.close()

    def fin():
        os.remove(sample_yaml_file.name)

    return sample_yaml_file

@pytest.fixture(scope="module")
def pysettings_file():
    test_data = """
ABC = 123
BUH_BUH = "BUH"
EASY_AS = ["do", "re", "mi"]
OR_SIMPLE_AS = {"do re mi": "abc, one, two, three"}
should_be_ignored = "YOU CAN'T SEE ME"
"""
    sample_pysettings_file = tempfile.NamedTemporaryFile(
        suffix='.py',
        dir='/tmp',
        delete=False
    )
    sample_pysettings_file.write(test_data.encode('utf-8'))
    sample_pysettings_file.close()

    def fin():
        os.remove(sample_pysettings_file.name)

    return sample_pysettings_file


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


class TestEnv:
    def test_init_formats_input_keys(self):
        env = Env(keys=["abc"])

        assert env.keys == ["ABC"]

    def test_load_with_existing_env_vars(self):
        env = Env(keys=['ABC'])
        os.environ['ABC'] = '456'
        env.load()

        assert env.data['ABC'] == '456'

        del os.environ['ABC']

    def test_load_with_non_existing_env_vars(self):
        env = Env(keys=["abc", "easy as"])
        os.environ["ABC"] = "123"

        env.load() 

        assert "ABC" in env.data
        assert "EASY_AS" not in env.data
        assert env.data["ABC"] == "123"

        del os.environ['ABC']

    def test_load_with_provided_overriding_keys(self):
        env = Env(keys=["abc"])

        os.environ["ABC"] = "123"
        os.environ["EASY_AS"] = "do re mi"

        env.load(keys=["easy as"])

        assert "ABC" in env.data
        assert "EASY_AS" in env.data
        assert env.data["ABC"] == "123"
        assert env.data["EASY_AS"] == "do re mi"

class TestFile:
    def test_load_with_json_file(self, json_file):
        fadapter = File(json_file.name)
        fadapter.load()

        assert 'ABC' in fadapter.data
        assert fadapter.data['ABC'] == '123'

    def test_load_with_yaml_file(self, yaml_file):
        fadapter = File(yaml_file.name)
        fadapter.load()
        assert 'ABC' in fadapter.data
        assert fadapter.data['ABC'] == '123'

    def test_load_with_pysettings_file_loads_uppercased_locales(self, pysettings_file):
        fadapter = File(pysettings_file.name)
        fadapter.load()

        assert "ABC" in fadapter.data
        assert "BUH_BUH" in fadapter.data
        assert "EASY_AS" in fadapter.data
        assert "OR_SIMPLE_AS" in fadapter.data

        assert isinstance(fadapter.data["ABC"], int)
        assert isinstance(fadapter.data["BUH_BUH"], str)
        assert isinstance(fadapter.data["EASY_AS"], list)
        assert isinstance(fadapter.data["OR_SIMPLE_AS"], dict)

        assert fadapter.data["ABC"] == 123
        assert fadapter.data["BUH_BUH"] == "BUH"
        assert fadapter.data["EASY_AS"] == ["do", "re", "mi"]
        assert fadapter.data["OR_SIMPLE_AS"] == {"do re mi": "abc, one, two, three"}


    def test_load_with_pysettings_file_ignores_lowercased_locales(self, pysettings_file):
        fadapter = File(pysettings_file.name)
        fadapter.load()

        assert "should_be_ignored" not in fadapter.data

class TestModule:
    def test_load_os_module_constants(self):
        madapter = Module(os)
        madapter.load()

        assert "WSTOPSIG" in madapter.data
        assert "WTERMSIG" in madapter.data
        assert "WNOHANG" in madapter.data

        assert "abort" not in madapter.data
        assert "access" not in madapter.data
        assert "altsep" not in madapter.data

    def test_init_with_invalid_mod_type_raises(self):
        with pytest.raises(TypeError):
            madapter = Module(123)


class TestDefaults:
    def test_load(self):
        d = Defaults({"abc": "123"})
        d.load()
        assert "ABC" in d.data
        assert d.data["ABC"] == "123"
