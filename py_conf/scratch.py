from py_conf.config import Config
from py_conf.sources.files import JsonSource
from py_conf.value import value


class TestConfig(Config):
    name: str = value(default='joe', override='bob', prompt=True)
    quantity: int = value(default=5, prompt=True)
    job: str = value()


if __name__ == '__main__':
    conf = TestConfig(sources=[JsonSource('test.json', '..')]).load()

    print(conf.name)
    print(conf.quantity)
    print(conf.job)
