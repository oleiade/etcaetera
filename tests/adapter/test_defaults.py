from etcaetera.adapter import Defaults 


class TestDefaults:
    def test_load(self):
        d = Defaults({"abc": "123"})
        d.load()
        assert "ABC" in d.data
        assert d.data["ABC"] == "123"
