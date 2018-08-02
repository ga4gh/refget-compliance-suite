import requests


SEQUENCE_ACCEPT_HEADER = {
    'Accept': 'text/vnd.ga4gh.seq.v1.0.0+plain'
}
SEQUENCE_MD5 = 'sequence/6681ac2f62509cfc220d78751b8dc524'
SEQUENCE_TRUNC512 = 'sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7'
SEQUENCE_CIRCULAR = 'sequence/3332ed720ac7eaa9b3655c06f6b9e196'


def sequence_implement(test, runner):
    '''Test to check if server returns 200 using I test sequence and
    appropriate headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + SEQUENCE_MD5, headers=SEQUENCE_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def sequence_implement_default(test, runner):
    '''Test to check if server returns 200 using I test sequence and
    no headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + SEQUENCE_MD5, headers=SEQUENCE_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def sequence_query_by_trunc512(test, runner):
    '''Test to check if server returns 200 using I test sequence trunc512 and
    appropriate headers if the server supports trunc512
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    if session_params['trunc512'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server does not support TRUNC512 algorithm')
        return
    response = requests.get(base_url + SEQUENCE_MD5, headers=SEQUENCE_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def sequence_invalid_checksum_404_error(test, runner):
    '''Test to check if server returns 404 using some garbage checksum and
    appropriate headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + 'sequence/Garbagechecksum', headers=SEQUENCE_ACCEPT_HEADER)
    if response.status_code == 404:
        test.result = 1
    else:
        test.result = -1


def sequence_invalid_encoding_415_error(test, runner):
    '''Test to check if server returns 200 using I test sequence and
    grabage encoding in Accept header
    '''
    base_url = str(runner.base_url)
    response = requests.get(
        base_url + SEQUENCE_MD5,
        headers={'Accept': 'embl/some_json'})
    if response.status_code == 415:
        test.result = 1
    else:
        test.result = -1


def sequence_start_end(test, runner):
    '''Test to check if server returns 200 and appropriate text using I test
    sequence and start/end query params set to 10 and 20 repectively
    '''
    base_url = str(runner.base_url)
    response = requests.get(
        base_url + SEQUENCE_MD5 + '?start=10&end=20',
        headers=SEQUENCE_ACCEPT_HEADER)
    if response.status_code == 200 and response.text == 'CCCACACACC':
        test.result = 1
    else:
        test.result = -1


def sequence_start_end_success_cases(test, runner):
    '''Test to check if server passes all the edge cases related to success
    queries using start/end params
    '''
    data = runner.test_data
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        print(_input)
        print(_output)
        response = requests.get(
            base_url + SEQUENCE_MD5 + _input[0],
            headers=SEQUENCE_ACCEPT_HEADER)
        case_output_object = {
            'expectation': data[0].sequence[_input[1]:_input[2]],
            'response': response.text,
            'expected_code': 200,
            'reponse_status_code': response.status_code
        }
        if response.status_code == 200 and \
                response.text == data[0].sequence[_input[1]:_input[2]] and \
                int(response.headers['content-length']) == _output:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_ouputs.append(case_output_object)


def sequence_range(test, runner):
    '''Test to check if server returns 200 and appropriate text using I test
    sequence and range header set to 10 and 19 repectively
    '''
    base_url = str(runner.base_url)
    header = {
        'Accept': 'text/vnd.ga4gh.seq.v1.0.0+plain',
        'Range': 'bytes=10-19'
    }
    response = requests.get(
        base_url + SEQUENCE_MD5, headers=header)
    if response.status_code == 206 and response.text == 'CCCACACACC':
        test.result = 1
    else:
        test.result = -1


def sequence_range_success_cases(test, runner):
    '''Test to check if server passesall the edge cases related to range header
    success queries
    '''
    data = runner.test_data
    header = {
        'Accept': 'text/vnd.ga4gh.seq.v1.0.0+plain',
    }
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        print(_input)
        print(_output)
        header['Range'] = _input[0]
        response = requests.get(
            base_url + SEQUENCE_MD5, headers=header)
        case_output_object = {
            'expectation': data[0].sequence[_input[1]:_input[2] + 1],
            'response': response.text,
            'expected_code': _output[0],
            'reponse_code': response.status_code
        }
        if response.status_code == _output[0] and \
                response.text == data[0].sequence[_input[1]:_input[2] + 1] \
                and int(response.headers['content-length']) == _output[1]:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_ouputs.append(case_output_object)