from py_conf.config import Config
from py_conf.value import value


class TestConfig(Config):
    name: str = value(default='joe', override='bob')
    quantity: int = 5
    job: str


if __name__ == '__main__':
    conf = TestConfig().load()

    print(conf.name)
    print(conf.quantity)
    print(conf.job)
