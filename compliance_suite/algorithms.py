import requests
import json


def base_algorithm(test, runner):
    if True is True:
        test.result = 1


def info_implement(test, runner):
    base_url = str(runner.base_url)
    api = 'sequence/service-info'
    response = requests.get(base_url + api)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def info_implement_default(test, runner):
    base_url = str(runner.base_url)
    api = 'sequence/service-info'
    response = requests.get(base_url + api)
    if response.status_code == 200:
        test.result = 1
    else:
        test.result = -1


def info_circular(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    api = 'sequence/service-info'
    response = requests.get(base_url + api)
    service_info_object = json.loads(response.text)["service"]
    if "circular_supported" in service_info_object:
        test.result = 1
        if service_info_object['circular_supported'] == 'true':
            session_params['circular_supported'] = True
        else:
            session_params['circular_supported'] = False
    else:
        test.result = -1


def info_algorithms(test, runner):
    base_url = str(runner.base_url)
    # session_params = runner.session_params
    api = 'sequence/service-info'
    response = requests.get(base_url + api)
    service_info_object = json.loads(response.text)["service"]
    if "algorithms" in service_info_object:
        test.result = 1
        # if service_info_object['algorithms'] == 'true':
        #     session_params['trunc512'] = True
        # else:
        #     session_params['trunc512'] = False
    else:
        test.result = -1


def info_subsequence(test, runner):
    base_url = str(runner.base_url)
    session_params = runner.session_params
    api = 'sequence/service-info'
    response = requests.get(base_url + api)
    service_info_object = json.loads(response.text)["service"]
    if "subsequence_limit" in service_info_object:
        test.result = 1
        session_params['subsequence_limit'] = int(service_info_object['subsequence_limit'])
    else:
        test.result = -1


def info_api_version(test, runner):
    base_url = str(runner.base_url)
    api = 'sequence/service-info'
    response = requests.get(base_url + api)
    service_info_object = json.loads(response.text)["service"]
    if "supported_api_versions" in service_info_object:
        test.result = 1
    else:
        test.result = -1
