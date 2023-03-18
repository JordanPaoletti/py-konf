from py_conf.config import Config
from py_conf.sources.files import ConfigSource
from py_conf.value import value


class TestConfig(Config):
    name: str = value(default='joe', override='bob')
    quantity: int = value(default=5)
    job: str = value()


if __name__ == '__main__':
    conf = TestConfig(sources=[ConfigSource('test.conf', path='..')]).load()

    print(conf.name)
    print(conf.quantity)
    print(conf.job)
