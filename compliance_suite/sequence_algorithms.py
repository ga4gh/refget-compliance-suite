import requests

SEQUENCE_ACCEPT_HEADER = {
    'Accept': 'text/vnd.ga4gh.refget.v1.0.0+plain'
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
        test.fail_text = test.fail_text + str(response.status_code)


def sequence_invalid_encoding_406_error(test, runner):
    '''Test to check if server returns 200 using I test sequence and
    garbage encoding in Accept header
    '''
    base_url = str(runner.base_url)
    response = requests.get(
        base_url + SEQUENCE_MD5,
        headers={'Accept': 'embl/some_json'})
    if response.status_code == 406:
        test.result = 1
    else:
        test.result = -1
        test.fail_text = test.fail_text + str(response.status_code)


def sequence_start_end(test, runner):
    '''Test to check if server returns 200 and appropriate text using I test
    sequence and start/end query params set to 10 and 20 respectively
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
        response = requests.get(
            base_url + SEQUENCE_MD5 + _input[0],
            headers=SEQUENCE_ACCEPT_HEADER)
        case_output_object = {'api': SEQUENCE_MD5 + ':' + _input[0] + ':' + str(SEQUENCE_ACCEPT_HEADER)}
        if response.status_code == 200 and \
                response.text == data[0].sequence[_input[1]:_input[2]] and \
                int(response.headers['content-length']) == _output:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)


def sequence_range(test, runner):
    '''Test to check if server returns 200 and appropriate text using I test
    sequence and range header set to 10 and 19 respectively
    '''
    base_url = str(runner.base_url)
    header = {
        'Accept': 'text/vnd.ga4gh.refget.v1.0.0+plain',
        'Range': 'bytes=10-19'
    }
    response = requests.get(
        base_url + SEQUENCE_MD5, headers=header)
    if response.status_code == 206 and response.text == 'CCCACACACC':
        test.result = 1
    else:
        test.result = -1


def sequence_range_success_cases(test, runner):
    '''Test to check if server passes all the edge cases related to range header
    success queries
    '''
    data = runner.test_data
    header = {
        'Accept': 'text/vnd.ga4gh.refget.v1.0.0+plain',
    }
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        header['Range'] = _input[0]
        response = requests.get(
            base_url + SEQUENCE_MD5, headers=header)
        case_output_object = {'api': SEQUENCE_MD5 + ':' + _input[0] + ':' + str(SEQUENCE_ACCEPT_HEADER)}
        if response.status_code == _output[0] and \
                response.text == data[0].sequence[_input[1]:_input[2] + 1] \
                and int(response.headers['content-length']) == _output[1]:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)


def sequence_circular(test, runner):
    '''Test to check if server passes all the edge cases related to circular queries
    '''
    session_params = runner.session_params
    if session_params['circular_supported'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server does not support circular sequences')
        return
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        response = requests.get(
            base_url + SEQUENCE_CIRCULAR + _input, headers=SEQUENCE_ACCEPT_HEADER)
        case_output_object = {'api': SEQUENCE_CIRCULAR + _input + ':' + str(SEQUENCE_ACCEPT_HEADER)}
        if response.status_code == 200 and \
                response.text == _output[0] \
                and int(response.headers['content-length']) == _output[1]:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)


def sequence_start_end_errors(test, runner):
    '''Test to check if server passes all the edge cases related start-end
    error cases
    '''
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        response = requests.get(
            base_url + 'sequence/' + _input[0] + _input[1], headers=SEQUENCE_ACCEPT_HEADER)
        case_output_object = {'api': 'sequence/' + _input[0] + ':' + _input[1]}
        if response.status_code == _output:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)


def sequence_range_errors(test, runner):
    '''Test to check if server passes all the edge cases related range
    error cases
    '''
    header = {
        'Accept': 'text/vnd.ga4gh.refget.v1.0.0+plain',
    }
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        header['Range'] = _input[1]
        response = requests.get(
            base_url + 'sequence/' + _input[0], headers=header)
        case_output_object = {'api': _input[0] + ':' + _input[1]}
        if response.status_code == _output:
            case_output_object['result'] = 1
        else:
            res = -1
            error = False
            successful_response = False
            squid = False
            if _output >= 400 and _output < 500:
                error = True
            if response.status_code == 200 or response.status_code == 206:
                successful_response = True
            if 'via' in response.headers and 'squid' in response.headers['via'].lower():
                squid = True
            # Squid sniffing:
            # Squid will strip range headers where the format of the range
            # was not valid and instead respond with the whole resource.
            # This breaks some of the tests we apply when giving an implementation
            # bad Accept headers. So first we look if we were testing for an
            # error code (4XX), see if we had a successful response
            # and the request was sent via squid then
            if error and successful_response and squid:
                res = 0
            case_output_object['result'] = res
            test.result = res
        test.case_outputs.append(case_output_object)


def sequence_circular_support_false_errors(test, runner):
    '''Test to check if server throws correct error codes on circular sequence
    query if server does not support circular sequences
    '''
    session_params = runner.session_params
    if session_params['circular_supported'] is True:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server supports circular sequences')
        return
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        response = requests.get(
            base_url + 'sequence/' + _input[0] + _input[1], headers=SEQUENCE_ACCEPT_HEADER)
        case_output_object = {'api': 'sequence/' + _input[0] + ':' + _input[1]}
        if response.status_code == _output:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)


def sequence_circular_support_true_errors(test, runner):
    '''Test to check if server throws correct error codes on circular sequence
    query if server supports circular sequences
    '''
    session_params = runner.session_params
    if session_params['circular_supported'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server does not support circular sequences')
        return
    base_url = str(runner.base_url)
    test.result = 1
    for case in test.cases:
        _input = case[0]
        _output = case[1]
        response = requests.get(
            base_url + 'sequence/' + _input[0] + _input[1], headers=SEQUENCE_ACCEPT_HEADER)
        case_output_object = {'api': 'sequence/' + _input[0] + ':' + _input[1]}
        if response.status_code == _output:
            case_output_object['result'] = 1
        else:
            case_output_object['result'] = -1
            test.result = -1
        test.case_outputs.append(case_output_object)
