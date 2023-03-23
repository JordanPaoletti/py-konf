import os
from dataclasses import dataclass
from typing import List

from py_konf.config import Config, value


class TestEnvVarSource:
    def test_types(self):
        @dataclass
        class Csv:
            vals: List[str]

        class Conf(Config):
            a: str
            b: int
            c: float
            d: bool
            e: Csv = value(from_str=lambda v: Csv(v.split(',')))

        os.environ['A'] = 'a'
        os.environ['B'] = '5'
        os.environ['C'] = '5.2'
        os.environ['D'] = 'True'
        os.environ['E'] = 'a,b,c'

        conf = Conf().load()

        conf.a = 'a'
        conf.b = '5'
        conf.c = '5.2'
        conf.d = 'True'
        conf.e.vals[0] = 'a'
        conf.e.vals[1] = 'b'
        conf.e.vals[2] = 'c'

    def test_source(self):
        class Conf(Config):
            name: str = 'test'
            age: int = value(default=3)
            job: str

        class Conf2(Config):
            name: str = 'test'
            age: int = value(default=3)
            job: str

        conf = Conf()
        conf2 = Conf2(name='conf2')

        os.environ['NAME'] = 'conf'
        os.environ['AGE'] = '1'
        os.environ['CONF2_NAME'] = 'conf2'
        os.environ['CONF2_AGE'] = '2'
        os.environ['CONF2_JOB'] = 'conf2'

        conf.load()
        conf2.load()

        assert conf.name == 'conf'
        assert conf.age == 1
        assert conf.job is None
        assert conf2.name == 'conf2'
        assert conf2.age == 2
        assert conf2.job == 'conf2'
