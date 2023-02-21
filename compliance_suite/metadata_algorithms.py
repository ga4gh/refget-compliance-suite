import requests
import json

# Some variables for not repeating the same thing

METADATA_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.refget.v1.0.0+json,application/vnd.ga4gh.refget.v2.0.0+json'
}
SEQ_MD5 = '6681ac2f62509cfc220d78751b8dc524/metadata'
SEQ_TRUNC512 = '959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/metadata'
SEQ_GA4GH = 'ga4gh:SQ.lZyxiD_ByprhOUzrR1o1bq0ezO_1gkrn/metadata'
SEQ_ALGO = {'md5': SEQ_MD5, 'trunc512': SEQ_TRUNC512, 'ga4gh': SEQ_GA4GH}
SEQ_INSDC = 'insdc:BK006935.2/metadata'
SEQ_IDENT = {'insdc': 'insdc:BK006935.2/metadata'}
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


def _metadata_query_by_algorithm(test, runner, algorithm, optional):
    '''
    Test if metadata endpoint returns 200 using specific algorithm with I test sequence
    if the server supports. Value stored in session_params. If not skip test
    and set skip text appropriately
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    if optional and session_params.get(f'algorithms:{algorithm}', False) is False:
        test.result = 0
        test.set_skip_text(str(test) + f' is skipped because server does not support {algorithm.upper()} algorithm')
        return
    response = requests.get(base_url + 'sequence/' + SEQ_ALGO.get(algorithm), headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1

def metadata_implement_default(test, runner):
    '''
    Test if metadata endpoint returns 200 without headers using I test sequence
    '''
    _metadata_query_by_algorithm(test, runner, 'md5', optional=False)


def metadata_query_by_trunc512(test, runner):
    '''
    Test if metadata endpoint returns 200 using trunc512 with I test sequence
    if the server supports. Value stored in session_params. If not skip test
    and set skip text appropriately
    '''
    _metadata_query_by_algorithm(test, runner, 'trunc512', optional=True)


def metadata_query_by_ga4gh(test, runner):
    '''
    Test if metadata endpoint returns 200 using ga4gh with I test sequence
    if the server supports. Value stored in session_params. If not skip test
    and set skip text appropriately
    '''
    _metadata_query_by_algorithm(test, runner, 'ga4gh', optional=True)


def _metadata_query_by_identifier(test, runner, identifier):
    '''
    Test if metadata endpoint returns 200 using specific algorithm with I test sequence
    if the server supports. Value stored in session_params. If not skip test
    and set skip text appropriately
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    if session_params[f'identifier_types:{identifier}'] is False:
        test.result = 0
        test.set_skip_text(str(test) + f' is skipped because server does not support {identifier.upper()} algorithm')
        return
    response = requests.get(base_url + 'sequence/' + SEQ_IDENT.get(identifier), headers=METADATA_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def metadata_query_by_insdc(test, runner):
    '''
    Test if metadata endpoint returns 200 using insdc identifier with I test sequence
    if the server supports. Value stored in session_params. If not skip test
    and set skip text appropriately
    '''
    _metadata_query_by_identifier(test, runner, 'insdc')


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


def metadata_by_algorithm(test, runner, algorithm, optional):
    '''
    Test if the algorithm is present in metadata response object. Skip if server does not
    support this algorithm
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    test.result = -1
    if optional and session_params[f'algorithms:{algorithm}'] is False:
        test.result = 0
        test.set_skip_text(str(test) + f' is skipped because "{algorithm}" is not supported by the server')
        return
    metadata_object = None
    try:
        response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if metadata_object[algorithm]:
            test.result = 1
    except:
        pass
    test.fail_text = test.fail_text + str(metadata_object)


def metadata_md5(test, runner):
    '''
    Test if md5 in metadata response object
    '''
    metadata_by_algorithm(test, runner, 'md5', optional=False)


def metadata_trunc512(test, runner):
    '''
    Test if trunc512 in metadata response object. Skip if server does not
    support trunc512
    '''
    metadata_by_algorithm(test, runner, 'trunc512', optional=True)


def metadata_ga4gh(test, runner):
    '''
    Test if ga4gh in metadata response object. Skip if server does not
    support ga4gh
    '''
    metadata_by_algorithm(test, runner, 'ga4gh', optional=True)


def metadata_insdc(test, runner):
    '''
    Test if insdc in metadata response aliases. Skip if server does not
    support insdc identifiers
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    test.result = -1
    if session_params['identifier_types:insdc'] is False:
        test.result = 0
        test.set_skip_text(str(test) + ' is skipped because "insdc" is not supported by the server')
        return
    metadata_object = None
    try:
        response = requests.get(base_url + 'sequence/' + SEQ_INSDC, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        aliases = metadata_object.get("aliases", {})
        if 'insdc' in [a.get('naming_authority') for a in aliases]:
            test.result = 1
    except:
        test.fail_text = test.fail_text + str(metadata_object)


def metadata_length(test, runner):
    '''
    Test if length in metadata response object
    '''
    base_url = str(runner.base_url)
    test.result = -1
    metadata_object = None
    try:
        response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "length" in metadata_object and metadata_object['length'] == 230218:
            test.result = 1
            return
    except:
        pass
    test.fail_text = test.fail_text + str(metadata_object)


def metadata_aliases(test, runner):
    '''
    Test if aliases in metadata response object
    '''
    base_url = str(runner.base_url)
    test.result = -1
    metadata_object = None
    try:
        response = requests.get(base_url + 'sequence/' + SEQ_MD5, headers=METADATA_ACCEPT_HEADER)
        metadata_object = json.loads(response.text)["metadata"]
        if "aliases" in metadata_object:
            test.result = 1
            return
    except:
        pass
    test.fail_text = test.fail_text + str(metadata_object)


def metadata_invalid_checksum_400_404_error(test, runner):
    '''
    Test if 400 or 404 on invalid checksum in metadata response
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + 'sequence/' + 'Garbagechecksum/metadata', headers=METADATA_ACCEPT_HEADER)
    if response.status_code in [400, 404]:
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
