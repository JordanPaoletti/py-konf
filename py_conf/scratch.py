from py_conf.config import Config
from py_conf.sources.cli import CliSource
from py_conf.value import value


class TestConfig(Config):
    name: str = value(default='joe', override='bob')
    quantity: int = value(default=5, cli_arg=('-q', '--quantity'))
    job: str = value(cli_arg='--job')


if __name__ == '__main__':
    conf = TestConfig(sources=[CliSource()]).load()

    print(conf.name)
    print(conf.quantity)
    print(conf.job)
