from py_konf.config import Config, value
from py_konf.sources.cli import CliSource


class TestCliSource:
    class Conf(Config):
        name: str = value(default='bob', cli_arg='--name')
        age: int = value(default=3, cli_arg=('-a', '--age'))
        employed: bool = value(cli_arg='-e')
        job: str = 'tester'

    def test_flag(self):
        args = ['--name', 'joe', '--job', 'not cli-able', '--age', '1', '-e']
        conf = self.Conf(sources=[CliSource(args=args)]).load()

        assert conf.name == 'joe'
        assert conf.age == 1
        assert conf.employed
        assert conf.job == 'tester'

    def test_source(self):
        args = ['--name', 'joe', '--job', 'not cli-able', '-a', '1']
        conf = self.Conf(sources=[CliSource(args=args)]).load()

        assert conf.name == 'joe'
        assert conf.age == 1
        assert conf.employed is None
        assert conf.job == 'tester'
