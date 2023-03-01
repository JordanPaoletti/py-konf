import pytest

import files as f
import py_conf.test.conftest as conf


class TestFiles:
    @pytest.fixture(autouse=True)
    def before_each(self):
        self.res_dir = f'{conf.RES_DIR}/files'

    def test_fetch_json(self):
        data = f.fetch_json(f'{self.res_dir}/json.json')
        assert data['abc'] == 'def'
        assert data['gab'] == 5
