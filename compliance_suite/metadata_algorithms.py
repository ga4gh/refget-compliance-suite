import requests
import json

METADATA_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.seq.v1.0.0+json'
}
METADATA_API = 'sequence'
SEQ_MD5 = '6681ac2f62509cfc220d78751b8dc524/metadata'
SEQ_TRUNC512 = '959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/metadata'
SEQ_CIRCULAR = '3332ed720ac7eaa9b3655c06f6b9e196/metadata'


def metadata_implement(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + METADATA_API + '/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_implement_default(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + METADATA_API + '/' + SEQ_MD5)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_query_by_trunc512(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    if session_params['trunc512'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server does not support TRUNC512 algorithm')
        return
    response = requests.get(base_url + METADATA_API + '/' + SEQ_TRUNC512, headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_query_circular_sequence(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    if session_params['circular_supported'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because server does not support circular sequences')
        return
    response = requests.get(base_url + METADATA_API + '/' + SEQ_CIRCULAR, headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_md5(test, runner):
    base_url = str(runner.base_url)
    test.result = -1
    response = requests.get(base_url + METADATA_API + '/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
    try:
        metadata_object = json.loads(response.text)["metadata"]
        if "md5" in metadata_object:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_trunc512(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    test.result = -1
    if session_params['trunc512'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because key "trunc512" although it is supported by the server')
        return
    try:
        response = requests.get(base_url + METADATA_API + '/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "trunc512" in metadata_object:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_length(test, runner):
    base_url = str(runner.base_url)
    test.result = -1
    try:
        response = requests.get(base_url + METADATA_API + '/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "length" in metadata_object and metadata_object['length'] == 230218:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_aliases(test, runner):
    base_url = str(runner.base_url)
    test.result = -1
    try:
        response = requests.get(base_url + METADATA_API + '/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "aliases" in metadata_object:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_invalid_checksum_404_error(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + METADATA_API + '/' + 'some1111garbage1111ID', headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 404:
        test.result = 1
    else:
        test.result = -1
        test.fail_text = test.fail_text + response.status_code


def metadata_invalid_encoding_415_error(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(
        base_url + METADATA_API + '/' + SEQ_MD5,
        headers={'Accept': 'embl/some_json'})
    if response.status_code == 415:
        test.result = 1
    else:
        test.result = -1
        test.fail_text = test.fail_text + response.status_code
