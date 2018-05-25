import pytest
import requests

###############################################################################
# Generic Error Conditions


@pytest.mark.parametrize("_input, _output", [
    (['some1111garbage1111ID', '', {}], 404),
    (['some1111garbage1111ID', '', {'Accept': 'text/embl'}], 404),
    (['some1111garbage1111ID', '?start=1&end=10', {'Accept': 'text/embl'}], 404),

    (['6681ac2f62509cfc220d78751b8dc524', '', {'Accept': 'text/embl'}], 415),
    (['6681ac2f62509cfc220d78751b8dc524', '?start=0&end=abc', {'Accept': 'text/embl'}], 415),
    (['6681ac2f62509cfc220d78751b8dc524', '?start=0&end=20', {'Accept': 'text/embl', 'Range':'bytes=0-20'}], 415),
    
    (['6681ac2f62509cfc220d78751b8dc524', '?start=0&end=10', {'Range': 'bytes=0-10'}], 400),

])
def test_sequence_generic_errors(server, data, _input, _output):
    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + _input[1], headers=_input[2])
    assert response.status_code == _output


###############################################################################
# start End error conditions


@pytest.mark.parametrize("_input, _output", [
    (['6681ac2f62509cfc220d78751b8dc524', '?start=abc&end=20', {}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '?start=-10&end=-29', {}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '?start=abc', {}], 400),

    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=67&end=5385', {}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5384&end=5385', {}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5384&end=5384', {}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5384&end=5', {}], 416),

    pytest.mark.skipif(
        ("pytest.config.getoption('--cir') != 'False'"))((
            ['6681ac2f62509cfc220d78751b8dc524', '?start=220218&end=671', {}], 501)),
    pytest.mark.skipif(
        ("pytest.config.getoption('--cir') != 'False'"))((
            ['3332ed720ac7eaa9b3655c06f6b9e196', '?start=20&end=4', {}], 501)),
    pytest.mark.skipif(
        ("pytest.config.getoption('--cir') == 'False'"))((
            ['6681ac2f62509cfc220d78751b8dc524', '?start=220218&end=671', {}], 416))
])
def test_sequence_start_end_errors(server, data, _input, _output):
    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + _input[1], headers=_input[2])
    assert response.status_code == _output


###############################################################################
# Range Header error conditions


@pytest.mark.parametrize("_input, _output", [
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'units=20-30'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=ab-19'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=-10--19'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=10--19'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=-10-'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes==10-19'}], 400),

    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5200-19'}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=59-50'}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5383-5380'}], 416),

    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5385-5389'}], 400),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5384-5385'}], 400),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=9999-99999'}], 400)
])
def test_sequence_range_errors(server, data, _input, _output):
    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + _input[1], headers=_input[2])
    assert response.status_code == _output
