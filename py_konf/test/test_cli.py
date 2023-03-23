from io import StringIO

from py_konf.cli import prompt_val


class TestCli:
    class TestPromptVal:
        def test_default_populated(self, monkeypatch):
            expected = 'test'
            str_input = StringIO(f'{expected}\n')
            monkeypatch.setattr('sys.stdin', str_input)

            v = prompt_val('name', 'default')
            assert v == expected

        def test_default_blank(self, monkeypatch):
            expected = 'default'
            str_input = StringIO(f'\n')
            monkeypatch.setattr('sys.stdin', str_input)

            v = prompt_val('name', 'default')
            assert v == expected

        def test_no_default_repeat(self, monkeypatch):
            expected = 'test'
            str_input = StringIO(f'\n\n\n{expected}\n')
            monkeypatch.setattr('sys.stdin', str_input)

            v = prompt_val('name')
            assert v == expected

        def test_no_default_happy(self, monkeypatch):
            expected = 'test'
            str_input = StringIO(f'{expected}\n')
            monkeypatch.setattr('sys.stdin', str_input)

            v = prompt_val('name')
            assert v == expected
