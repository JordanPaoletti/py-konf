from py_conf.config import Config, value


class TestConfig:
    def test_defaults(self):
        class Conf(Config):
            name: str = 'test'
            age: int = value(default=3)
            job: str

        conf = Conf().load()
        assert conf.name == 'test'
        assert conf.age == 3
        assert conf.job is None

    def test_overrides(self):
        class Conf(Config):
            name: str = value(default='test', override='override')
            age: int = value(default=3, override=2)
            job: str = value(override='over')

        conf = Conf().load()
        assert conf.name == 'override'
        assert conf.age == 2
        assert conf.job == 'over'
