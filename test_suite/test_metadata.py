import json
import requests
import pytest

###############################################################################
# Successful Conditions


def get_metadata(seq, checksum):
    response = {
        "metadata": {
            "id": checksum,
            "length": seq.size,
            "alias": []
        }
    }
    response["metadata"]["alias"].append({"alias": seq.md5})
    response["metadata"]["alias"].append({"alias": seq.sha512})
    return json.dumps(response)


def check_complete_sequence_response(response, seq, checksum):
    assert response.text == get_metadata(seq, checksum)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/vnd.ga4gh.seq.v1.0.0+json'


def test_complete_sequence(server, data):
    api = 'sequence/'
    accept_header = {
        'Accept': 'text/vnd.ga4gh.seq.v1.0.0+json'
    }
    for seq in data:
        response = requests.get(
            server + api + seq.md5 + '/metadata', headers=accept_header)
        check_complete_sequence_response(response, seq, seq.md5)
        response = requests.get(server + api + seq.md5 + '/metadata')
        check_complete_sequence_response(response, seq, seq.md5)
        response = requests.get(server + api + seq.sha512 + '/metadata')
        check_complete_sequence_response(response, seq, seq.sha512)


###############################################################################
# Error Conditions


@pytest.mark.parametrize("_input, _output", [
    (['some1111garbage1111ID', {}], 404),
    (['some1111garbage1111ID', {'Accept': 'text/vnd.ga4gh.seq.v1.0.0+json'}], 404),
    (['some1111garbage1111ID', {'Accept': 'text/embl'}], 404),
    (['6681ac2f62509cfc220d78751b8dc524', {'Accept': 'text/embl'}], 415)

])
def test_sequence_generic_errors(server, data, _input, _output):
    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + '/metadata', headers=_input[1])
    assert response.status_code == _output
