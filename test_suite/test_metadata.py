import json
import requests

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
