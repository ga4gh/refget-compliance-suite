import pytest
from utils import get_seq_obj
from mockserver import start_mock_server, get_free_port

''' This is the first module which gets executed as we give the command py.test
It provides all the fixtures to the test suite. Fixtures can be viewed as the
setUp conditions for the test suite to run
'''


@pytest.fixture(scope='session')
def data():
    '''data fixture loads all the data and return data variabe for use in tests
    '''
    data = []
    data.append(get_seq_obj("I"))
    data.append(get_seq_obj("VI"))
    data.append(get_seq_obj("NC"))
    # print(data[0].size)
    # print(data[1].size)
    print(data[2].sequence)
    return data


def pytest_addoption(parser):
    '''pytest_addoption is used to define extra command line arguments. It
    defines currently 2 i.e. server, cir and redir(all optional)
    '''
    parser.addoption("--server", type="string")
    parser.addoption(
        "--cir",
        action="store_true", default="False", help="circular support")
    parser.addoption(
        "--redir",
        action="store_true",
        default="False", help="success queries redirection")
    parser.addoption(
        "--trunc512",
        action="store_true",
        default="False", help="trunc512 support")


@pytest.fixture(scope='session')
def server(request):
    '''server fixture returns the base url of the server to be tested. If the
    server is not given in the command line argument, then it uses mock server
    defined in mockserver.py for testing by calling its get_free_port and
    start_mock_server functions. circular_support is passed if mockserver is
    used to set the global variable in the mockserver.
    '''
    option = request.config.option
    if option.server is not None:
        return 'http://' + option.server + '/'
    circular_support = request.config.getoption("--cir")
    redirection = request.config.getoption("--redir")
    trunc512 = request.config.getoption("--trunc512")
    print(trunc512)
    port = get_free_port()
    start_mock_server(port, circular_support, redirection, trunc512=trunc512)
    server_base_url = 'http://localhost:' + str(port) + '/'
    return server_base_url
