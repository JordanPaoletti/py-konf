import os

import pytest

import py_konf.test.conftest as conftest
from py_konf.config import Config, value
from py_konf.sources.files import JsonSource, ConfigSource


class TestFiles:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.res_dir = f'{conftest.RES_DIR}/files'

    def test_config_source_multi_sects(self):
        class Conf(Config):
            a: int = 5
            b: str = value(default='hello')

        conf = Conf(
            sources=[ConfigSource(file_name='test.conf', section_name='config', path=self.res_dir)]
        ).load()

        assert conf.a == 1
        assert conf.b == 'conf'

    def test_config_source(self):
        class Conf(Config):
            a: int = 5
            b: str = value(default='hello')

        conf = Conf(
            sources=[ConfigSource(file_name='test.conf', path=self.res_dir)]
        ).load()

        assert conf.a == 1
        assert conf.b == 'conf'

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
