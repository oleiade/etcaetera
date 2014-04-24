import os
import json
import yaml
import pytest
import tempfile

from etcaetera.adapter import File


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


class TestFile:
    def test___init__with_strict_true_and_non_existing_filepath_raises(self):
        with pytest.raises(IOError):
            fadapter = File('abc 123 easy as 891n3idu91jwnd19dn129d', strict=True)

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

    def test_load_with_non_existing_file_in_strict_mode_raises(self):
        with pytest.raises(IOError):
            fadapter = File('/tmp/does/not/exist')  # Here safe is False
            fadapter.strict = True  # Change it to True for testing purposes
            fadapter.load()

    def test_load_with_non_existing_file_in_non_strict_mode_keeps_data_empty(self):
        fadapter = File('/tmp/does/not/exist')
        fadapter.strict = False
        fadapter.load()

        assert fadapter.data == {}
