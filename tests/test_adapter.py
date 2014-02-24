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
    json.dump(test_data, sample_json_file)
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
    yaml.dump(test_data, sample_yaml_file)
    sample_yaml_file.close()

    def fin():
        os.remove(sample_yaml_file.name)

    return sample_yaml_file


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


class TestDefaults:
    def test_load(self):
        d = Defaults({"abc": "123"})
        d.load()
        assert "abc" in d.data
        assert d.data["abc"] == "123"
