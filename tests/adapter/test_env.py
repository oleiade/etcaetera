import os

from etcaetera.adapter import Env


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


