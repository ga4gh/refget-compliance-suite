import requests
import json

# Some variables for not repeating the same thing

METADATA_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.refget.v1.0.0+json'
}
SEQ_MD5 = '6681ac2f62509cfc220d78751b8dc524/metadata'
SEQ_TRUNC512 = '959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/metadata'
SEQ_CIRCULAR = '3332ed720ac7eaa9b3655c06f6b9e196/metadata'


def metadata_implement(test, runner):
    '''
    Test if metadata endpoint returns 200 with appropriate headers using I test
    sequence
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_implement_default(test, runner):
    '''
    Test if metadata endpoint returns 200 without headers using I test sequence
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + 'sequence/' + SEQ_MD5)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_query_by_trunc512(test, runner):
    '''
    Test if metadata endpoint returns 200 using trunc512 with I test sequence
    if the server supports. Value stored in session_params. If not skip test
    and set skip text appropriately
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    if session_params['trunc512'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server does not support TRUNC512 algorithm')
        return
    response = requests.get(base_url + 'sequence/' + SEQ_TRUNC512, headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_query_circular_sequence(test, runner):
    '''
    Test if metadata endpoint returns 200 using circular test sequence
    if the server supports circular sequences. Value stored in session_params.
    If not skip test and set skip text appropriately
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    if session_params['circular_supported'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server does not support circular sequences')
        return
    response = requests.get(base_url + 'sequence/' + SEQ_CIRCULAR, headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_md5(test, runner):
    '''
    Test if md5 in metadata response object
    '''
    base_url = str(runner.base_url)
    test.result = -1
    response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
    try:
        metadata_object = json.loads(response.text)["metadata"]
        if "md5" in metadata_object:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_trunc512(test, runner):
    '''
    Test if trunc512 in metadata response object. Skip if server does not
    support trunc512
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    test.result = -1
    if session_params['trunc512'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because key "trunc512" although it is supported by the server')
        return
    try:
        response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "trunc512" in metadata_object:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_length(test, runner):
    '''
    Test if length in metadata response object
    '''
    base_url = str(runner.base_url)
    test.result = -1
    try:
        response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "length" in metadata_object and metadata_object['length'] == 230218:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_aliases(test, runner):
    '''
    Test if aliases in metadata response object
    '''
    base_url = str(runner.base_url)
    test.result = -1
    try:
        response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "aliases" in metadata_object:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_invalid_checksum_404_error(test, runner):
    '''
    Test if 404 on invalid checksum in metadata response
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + 'sequence/' + 'some1111garbage1111ID/metadata', headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 404:
        test.result = 1
    else:
        test.result = -1
        test.fail_text = test.fail_text + str(response.status_code)


def metadata_invalid_encoding_406_error(test, runner):
    '''
    Test if 406 on invalid encoding in Accept header
    '''
    base_url = str(runner.base_url)
    response = requests.get(
        base_url + 'sequence/' + SEQ_MD5,
        headers={'Accept': 'embl/some_json'})
    if response.status_code == 406:
        test.result = 1
    else:
        test.result = -1
        test.fail_text = test.fail_text + str(response.status_code)
