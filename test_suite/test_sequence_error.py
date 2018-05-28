import pytest
import requests

'''This module will be testing error queries associated with GET sequence by
checksum ID API. All the functions with 'test_' as prefix will be treated as
test cases by pytest.
'''

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
    '''test_sequence_generic_errors tests generic error codes associated with
    unknown checksum ID, unsupported encoding request in Accept header or both
    and using Range header and start - end query parameter simultaneously
    '''
    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + _input[1], headers=_input[2])
    assert response.status_code == _output


###############################################################################
# start End error conditions


@pytest.mark.parametrize("_input, _output", [
    # invalid input
    (['6681ac2f62509cfc220d78751b8dc524', '?start=abc&end=20', {}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '?start=-10&end=-29', {}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '?start=abc', {}], 400),

    # Range out of bounds. Size of the sequence being tested is 5384.
    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=67&end=5387', {}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5375', {}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5386', {}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5', {}], 416),

    # Edge cases depending on the implementation of the server tested and hence
    # skipif tag is used to skip tests appropriately
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
    '''test_sequence_start_end_errors tests all the error edge cases associated
    with using start - end query parameters.
    '''

    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + _input[1], headers=_input[2])
    assert response.status_code == _output


###############################################################################
# Range Header error conditions


@pytest.mark.parametrize("_input, _output", [
    # invalid input
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'units=20-30'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=ab-19'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=-10--19'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=10--19'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=-10-'}], 400),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes==10-19'}], 400),

    # Range out of bounds as fbs > lbs which is not allowed
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5200-19'}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=59-50'}], 416),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5385-5382'}], 416),

    # Range out of bounds. Size of the sequence tested is 5384
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5387-5391'}], 400),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=5386-5387'}], 400),
    (['3332ed720ac7eaa9b3655c06f6b9e196', '', {'Range': 'bytes=9999-99999'}], 400)
])
def test_sequence_range_errors(server, data, _input, _output):
    '''test_sequence_range_errors tests all the error edge cases associated
    with using range header.
    '''

    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + _input[1], headers=_input[2])
    assert response.status_code == _output
