from pytest import fixture


def pytest_addoption(parser):
    try:
        parser.addoption('--e2e', action='store_true', default=False)
    except Exception as ex:
        print(ex)
    
@fixture(scope='session')
def is_run_e2e(pytestconfig) -> bool:
    return pytestconfig.getoption('e2e')
    