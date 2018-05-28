import requests
import pytest

###############################################################################
# Test cases for complete sequence success queries


def check_complete_sequence_response(response, seq):
    assert response.text == seq.sequence
    assert response.status_code == 200
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
    assert response.headers['content-length'] == str(seq.size)


def test_complete_sequence(server, data):
    api = 'sequence/'
    accept_header = {
        'Accept': 'text/vnd.ga4gh.seq.v1.0.0+plain'
    }
    for seq in data:
        response = requests.get(server + api + seq.md5, headers=accept_header)
        check_complete_sequence_response(response, seq)
        response = requests.get(server + api + seq.md5)
        check_complete_sequence_response(response, seq)
        response = requests.get(server + api + seq.sha512)
        check_complete_sequence_response(response, seq)


###############################################################################
# Test cases for sub-sequence success queries using start-end parameters


@pytest.mark.parametrize("_input, _output", [
    ('?start=10&end=10', ['', 0]),
    ('?start=10&end=20', ['CCCACACACC', 10]),
    ('?start=10&end=11', ['C', 1]),
    ('?start=230208', ['TGTGTGTGGG', 10]),
    ('?end=5', ['CCACA', 5]),
    ('?start=230217&end=230218', ['G', 1]),
])
def test_subsequence_start_end_I(server, data, _input, _output):
    api = 'sequence/'
    response = requests.get(server + api + data[0].md5 + _input)
    assert response.text == _output[0]
    assert response.status_code == 200
    assert int(response.headers['content-length']) == _output[1]
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
    assert response.headers['accept-ranges'] == "none"


@pytest.mark.parametrize("_input, _output", [
    pytest.mark.skipif(
        ("pytest.config.getoption('--cir') == 'False'"))(('?start=5372&end=5', [
            'ATCCAACCTGCAGAGTT', 17]))
])
def test_subsequence_start_end_NC(server, data, _input, _output):
    api = 'sequence/'
    response = requests.get(server + api + data[2].md5 + _input)
    # print(server + api + data[2].md5 + _input)
    assert response.text == _output[0]
    assert response.status_code == 200
    assert int(response.headers['content-length']) == _output[1]
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'


###############################################################################
# Test cases for sub-sequence success queries using Range header


@pytest.mark.parametrize("_input, _output", [
    (['bytes=10-19', 10, 19], [206, 10]),
    (['bytes=10-230217', 10, 230217], [206, 230208]),
    (['bytes=10-999999', 10, 999999], [206, 230208]),
    (['bytes=0-230217', 0, 230217], [200, 230218]),
    (['bytes=0-999999', 0, 999999], [200, 230218]),
    (['bytes=0-0', 0, 0], [206, 1]),
    (['bytes=230217-230217', 230217, 230217], [206, 1])
])
def test_subsequence_range_I(server, data, _input, _output):
    api = 'sequence/'
    header = {'Range': _input[0]}
    response = requests.get(server + api + data[0].md5, headers=header)
    if _input[2] >= data[0].size:
        _input[2] = data[0].size - 1
    assert response.text == data[0].sequence[_input[1]:_input[2]+1]
    assert response.status_code == _output[0]
    assert int(response.headers['content-length']) == _output[1]
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
