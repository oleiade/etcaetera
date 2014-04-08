import pytest

from etcaetera.formatters import (
    uppercased,
    lowercased,
    environ
)


def test_uppercased_with_lowercased_str():
    assert uppercased.format("abc") == "ABC"


def test_uppercased_with_uppercased_str():
    assert uppercased.format("ABC") == "ABC"


def test_lowercased_with_uppercased_str():
    assert lowercased.format("ABC") == "abc"


def test_lowercased_with_lowercased_str():
    assert lowercased.format("abc") == "abc"


def test_environ():
    assert environ.format("aBc 123") == "ABC_123"
