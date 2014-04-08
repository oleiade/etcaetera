import pytest

from etcaetera.exceptions import MalformationError
from etcaetera.utils import (
   format_key,
   is_nested_key,
)


def test_format_env_key_with_mixed_case():
    assert format_key('abC 123') == 'ABC_123'


def test_format_env_key_with_lower_case():
    assert format_key('abc 123') == 'ABC_123'


def test_format_env_key_with_upper_case():
    assert format_key('ABC 123') == 'ABC_123'


def test_format_env_key_with_trailing_spaces():
    assert format_key('   abc 123  ') == 'ABC_123'


def test_is_nested_with_non_nested_key():
    assert is_nested_key('abc 123') is False


def test_is_nested_with_nested_key():
    assert is_nested_key('abc.123') is True


def test_is_nested_with_invalid_key_nesting_raises():
    with pytest.raises(MalformationError):
        is_nested_key('.abc.123')

    with pytest.raises(MalformationError):
        is_nested_key('abc.123.')

    with pytest.raises(MalformationError):
        is_nested_key('abc..123')
