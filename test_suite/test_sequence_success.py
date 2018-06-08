import requests
import pytest
from skipif_decorators import circular_support_false_skip,\
    redirection_true_skip, redirection_false_skip


def is_ascii(text):
    '''Checks if text is ascii
    '''
    return all(ord(char) < 128 for char in text)


'''This module will be testing success queries associated with GET sequence by
checksum ID API. All the functions with 'test_' as prefix will be treated as
test cases by pytest.
'''
###############################################################################
# Test Cases for complete seqeunce success queries


def check_complete_sequence_response(response, seq):
    '''check_complete_sequence_response is a utility function used by
    test_complete_sequence function to remove duplication of code. It takes
    response and seq object as input parameter and assert for reponse header,
    status code and content
    '''
    assert response.text == seq.sequence
    assert is_ascii(response.text) is True
    assert response.status_code == 200
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
    assert response.headers['content-length'] == str(seq.size)


@redirection_true_skip
def test_complete_sequence(server, data):
    '''test_complete_sequence tests all the possible scenarios of retrieving
    successfully retrieving complete sequences. It uses server and data fixture
    values from conftest.py module.
    '''

    api = 'sequence/'
    accept_header = {
        'Accept': 'text/vnd.ga4gh.seq.v1.0.0+plain'
    }
    for seq in data:
        # checking support for md5 with Accept headers
        response = requests.get(server + api + seq.md5, headers=accept_header)
        check_complete_sequence_response(response, seq)

        # checking support for md5 without Accept header
        response = requests.get(server + api + seq.md5)
        check_complete_sequence_response(response, seq)

        # checking support for truncated sha512 without Accept header
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
    '''test_subsequence_start_end_I tests all the possible scenarios of
    successfully retrieving sub-sequences using start and end query parameters.
    It uses server and data fixture values from conftest.py module.
    'parametrize' is also implemented to reuse same test code on different
    inputs.
    '''

    api = 'sequence/'
    response = requests.get(server + api + data[0].md5 + _input)
    assert response.text == _output[0]
    assert is_ascii(response.text) is True
    assert response.status_code == 200
    assert int(response.headers['content-length']) == _output[1]
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
    assert response.headers['accept-ranges'] == "none"


@pytest.mark.parametrize("_input, _output", [
    (['?start=0', 0, None], 230218),
    (['?&end=230218', None, 230218], 230218),
    (['?start=0&end=230218', 0, 230218], 230218),
    (['?start=1&end=230218', 1, 230218], 230217),
    (['?start=230217', 230217, None], 1),
    (['?end=0', None, 0], 0)
])
def test_subsequence_start_end_I_from_db(server, data, _input, _output):
    '''test_subsequence_start_end_I tests all the possible scenarios of
    successfully retrieving sub-sequences using start and end query parameters.
    It uses server and data fixture values from conftest.py module.
    'parametrize' is also implemented to reuse same test code on different
    inputs.
    '''

    api = 'sequence/'
    response = requests.get(server + api + data[0].md5 + _input[0])
    assert response.text == data[0].sequence[_input[1]:_input[2]]
    assert is_ascii(response.text) is True
    assert response.status_code == 200
    assert int(response.headers['content-length']) == _output
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
    assert response.headers['accept-ranges'] == "none"


@circular_support_false_skip
@pytest.mark.parametrize("_input, _output", [
    ('?start=5374&end=5', ['ATCCAACCTGCAGAGTT', 17]),
    ('?start=5374&end=0', ['ATCCAACCTGCA', 12]),
    ('?start=5380&end=25', ['CCTGCAGAGTTTTATCGCTTCCATGACGCAG', 31]),
])
def test_subsequence_start_end_NC(server, data, _input, _output):
    '''test_subsequence_start_end_NC tests a specific case when the server
    supports circular seqeunces. This test case will only run if '--cir' tag
    is specified and hence skipif function is used above which tells to skip
    this test if server does not support circular sequences.
    '''

    api = 'sequence/'
    response = requests.get(server + api + data[2].md5 + _input)
    assert response.text == _output[0]
    assert is_ascii(response.text) is True
    assert response.status_code == 200
    assert int(response.headers['content-length']) == _output[1]
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'


###############################################################################
# Test cases for sub-sequence success queries using Range header


@redirection_true_skip
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
    '''test_subsequence_range_I tests all the possible scenarios of successfully
    retrieving sub-sequences using range header. It uses server and data
    fixture values from conftest.py module.
    'parametrize' is also implemented to reuse same test code on different
    inputs.
    '''

    api = 'sequence/'
    header = {'Range': _input[0]}
    response = requests.get(server + api + data[0].md5, headers=header)

    # if the last-byte-spec is >= size, replace it with size - 1.
    if _input[2] >= data[0].size:
        _input[2] = data[0].size - 1

    assert response.text == data[0].sequence[_input[1]:_input[2]+1]
    assert is_ascii(response.text) is True
    assert response.status_code == _output[0]
    assert int(response.headers['content-length']) == _output[1]
    assert response.headers['content-type'] == \
        'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'


###############################################################################
# Test cases in case of redirection by the server

@redirection_false_skip
@pytest.mark.parametrize("_input, _output", [
    (['6681ac2f62509cfc220d78751b8dc524', '', {}], 301),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=0-20'}], 301),
    (['6681ac2f62509cfc220d78751b8dc524', '', {'Range': 'bytes=0-10'}], 301),

])
def test_sequence_redirect(server, data, _input, _output):
    '''test_sequence_redirect tests if the server sending a 301 status code on
    redirecting the request to some other URL (eg aws s3 bucket)
    '''
    api = 'sequence/'
    response = requests.get(
        server + api + _input[0] + _input[1], headers=_input[2],
        allow_redirects=False)
    assert response.status_code == _output
