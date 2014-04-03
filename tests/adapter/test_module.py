import os
import pytest
import tempfile

from etcaetera.adapter import Module


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
