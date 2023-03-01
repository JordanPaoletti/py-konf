from py_conf.config import Config, value


class TestConfig:
    def test_defaults(self):
        class Conf(Config):
            name: str = 'test'
            age: int = value(default=3)
            job: str

        conf = Conf()
        assert conf.name == 'test'
        assert conf.age == 3
        assert conf.job is None
