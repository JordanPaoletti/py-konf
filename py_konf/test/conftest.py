import pytest

ROOT_DIR = None
RES_DIR = None


@pytest.fixture(scope='session', autouse=True)
def prep_dirs(request):
    global ROOT_DIR, RES_DIR
    ROOT_DIR = request.config.rootdir
    RES_DIR = f'{ROOT_DIR}/test_res'
