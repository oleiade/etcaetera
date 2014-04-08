import pytest

from etcaetera.formatters import (
    uppercased,
    lowercased,
    environ
)


def test_uppercased_with_lowercased_str():
    assert uppercased("abc") == "ABC"


def test_uppercased_with_uppercased_str():
    assert uppercased("ABC") == "ABC"


def test_lowercased_with_uppercased_str():
    assert lowercased("ABC") == "abc"


def test_lowercased_with_lowercased_str():
    assert lowercased("abc") == "abc"


def test_environ():
    assert environ("aBc 123") == "ABC_123"
