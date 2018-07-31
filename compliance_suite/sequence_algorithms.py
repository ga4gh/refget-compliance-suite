import requests

SEQUENCE_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.seq.v1.0.0+json'
}
SEQUENCE_MD5 = 'sequence/6681ac2f62509cfc220d78751b8dc524'
SEQUENCE_TRUNC512 = 'sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7'
SEQUENCE_CIRCULAR = 'sequence/3332ed720ac7eaa9b3655c06f6b9e196'


def sequence_implement(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + SEQUENCE_MD5, headers=SEQUENCE_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def sequence_implement_default(test, runner):
    base_url = str(runner.base_url)
    response = requests.get(base_url + SEQUENCE_MD5, headers=SEQUENCE_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def sequence_query_by_trunc512(test, runner):
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
