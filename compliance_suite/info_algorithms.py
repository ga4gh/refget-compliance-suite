import requests
import json

# Some variables for not repeating the same thing

INFO_ACCEPT_HEADER = {
    'Accept': 'application/vnd.ga4gh.refget.v1.0.0+json'
}
INFO_API = 'sequence/service-info'


def info_implement(test, runner):
    '''
    Test to check if info-endpoint returns 200 OK with appropriate headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def info_implement_default(test, runner):
    '''
    Test to check if info-endpoint returns 200 OK without headers
    '''
    base_url = str(runner.base_url)
    response = requests.get(base_url + INFO_API)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def info_circular(test, runner):
    '''
    Test to check if info-endpoint has circular in the response object. And if
    it is there it updates session_params['circular'] as per the value
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    service_info_object = None
    try:
        service_info_object = json.loads(response.text)["service"]
        test.result = 1
        if service_info_object['circular_supported'] == True:
            session_params['circular_supported'] = True
        else:
            session_params['circular_supported'] = False
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)


def info_algorithms(test, runner):
    '''
    Test to check if info-endpoint has algorithms in the response object. And if
    it is there it updates session_params['trunc512'] as per the value
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    service_info_object = None
    try:
        service_info_object = json.loads(response.text)["service"]
        test.result = 1
        if 'trunc512' in service_info_object['algorithms']:
            session_params['trunc512'] = True
        else:
            session_params['trunc512'] = False
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)


def info_subsequence(test, runner):
    '''
    Test to check if info-endpoint has subsequence_limit in the response object.
    If the key is present we update session_params['subsequence_limit'] as per the
    value
    '''
    base_url = str(runner.base_url)
    session_params = runner.session_params
    service_info_object = None
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    try:
        service_info_object = json.loads(response.text)["service"]
        if service_info_object['subsequence_limit'] is not None:
            session_params['subsequence_limit'] = int(service_info_object['subsequence_limit'])
        test.result = 1
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)


def info_api_version(test, runner):
    '''
    Test to check if info-endpoint has supported_api_versions in the response
    object.
    '''
    service_info_object = None
    base_url = str(runner.base_url)
    response = requests.get(base_url + INFO_API, headers=INFO_ACCEPT_HEADER)
    try:
        service_info_object = json.loads(response.text)["service"]
        if "supported_api_versions" in service_info_object:
            test.result = 1
    except:
        test.result = -1
        test.fail_text = test.fail_text + str(service_info_object)
