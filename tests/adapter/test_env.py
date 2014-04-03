import os

from etcaetera.adapter import Env


class TestEnv:
    def test_init_with_args_sets_keys_attribute(self):
        env = Env("abc", "123", "easy_as")

        assert env.keys == ['ABC', '123', 'EASY_AS']
        assert env.items == {}

    def test_init_with_kwargs_sets_items_attribute(self):
        env = Env(**{"src_abc": "dest_abc", "src_easy_as": "dest_easy_as"})

        assert env.items == {
            "SRC_ABC": "DEST_ABC",
            "SRC_EASY_AS": "DEST_EASY_AS"
        }

    def test_load_with_existing_env_vars_from_args(self):
        env = Env('ABC')
        os.environ['ABC'] = '456'
        env.load()

        assert env.data['ABC'] == '456'

        del os.environ['ABC']

    def test_load_with_non_existing_env_vars_from_args(self):
        env = Env("abc", "easy as")
        os.environ["ABC"] = "123"

        env.load() 

        assert "ABC" in env.data
        assert "EASY_AS" not in env.data
        assert env.data["ABC"] == "123"

        del os.environ['ABC']

    def test_load_with_existing_env_vars_from_kwargs(self):
        env = Env(**{'src_abc': 'dest_abc'})
        os.environ['SRC_ABC'] = '456'
        env.load()

        assert 'SRC_ABC' not in env.data
        assert 'DEST_ABC' in env.data
        assert env.data['DEST_ABC'] == '456'

        del os.environ['SRC_ABC']

    def test_load_with_non_existing_env_vars_from_args(self):
        env = Env(**{"src_abc": "dest_abc", "src_easy_as": "dest_easy_as"})

        os.environ["SRC_ABC"] = "123"
        env.load() 

        assert "SRC_ABC" not in env.data
        assert "DEST_ABC" in env.data
        assert env.data["DEST_ABC"] == "123"

        assert "SRC_EASY_AS" not in env.data
        assert "DEST_EASY_AS" not in env.data

        del os.environ['SRC_ABC']

