import pytest

from etcaetera.utils import (
   format_key
)


def test_format_env_key_with_mixed_case():
    assert format_key('abC 123') == 'ABC_123'


def test_format_env_key_with_lower_case():
    assert format_key('abc 123') == 'ABC_123'


def test_format_env_key_with_upper_case():
    assert format_key('ABC 123') == 'ABC_123'


def test_format_env_key_with_trailing_spaces():
    assert format_key('   abc 123  ') == 'ABC_123'
