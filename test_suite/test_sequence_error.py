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
