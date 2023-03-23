from io import StringIO

from py_konf.config import Config, value


class TestPromptSource:
    def test_prompt(self, monkeypatch):
        class Conf(Config):
            first_name: str = value(default='joe', override='bob', prompt=True)
            last_name: str = value(default='last', override='fast', prompt=True)
            quantity: int = value(default=5, prompt=True)
            job: str = value(prompt=True)

        str_input = StringIO('\ntes\n3\n\ntest\n')
        monkeypatch.setattr('sys.stdin', str_input)

        conf = Conf().load()

        assert conf.first_name == 'bob'
        assert conf.last_name == 'tes'
        assert conf.quantity == 3
        assert conf.job == 'test'
