import os

import pytest

import py_conf.test.conftest as conftest
from py_conf.config import Config, value
from py_conf.sources.files import JsonSource


class TestFiles:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.res_dir = f'{conftest.RES_DIR}/files'

    def test_json_source(self):
        class Conf(Config):
            a: int = 5
            b: str = value(default='hello', override='test')

        conf = Conf(
            sources=[JsonSource(file_name='test.json', path=self.res_dir)]
        ).load()

        assert conf.a == 1
        assert conf.b == 'test'

    def test_json_source_env(self):
        class Conf(Config):
            a: int = 5
            b: str = value(default='hello', override='test')

        env_var = 'TEST'
        os.environ[env_var] = f'{self.res_dir}/alt'
        conf = Conf(
            sources=[JsonSource(file_name='test.json', path=self.res_dir, env_var=env_var)]
        ).load()

        assert conf.a == 2
        assert conf.b == 'test'