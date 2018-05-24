import pytest
from utils import get_seq_obj
from mockserver import start_mock_server, get_free_port


@pytest.fixture(scope='session')
def data():
    data = []
    data.append(get_seq_obj("I"))
    data.append(get_seq_obj("VI"))
    data.append(get_seq_obj("NC"))
    return data


def pytest_addoption(parser):
    parser.addoption("--server", type="string")


@pytest.fixture(scope='session')
def server(request):
    option = request.config.option
    if option.server is not None:
        return 'http://' + option.server + '/'
    port = get_free_port()
    start_mock_server(port)
    server_base_url = 'http://localhost:' + str(port) + '/'
    return server_base_url
