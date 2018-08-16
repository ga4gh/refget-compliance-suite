import requests
import json
import pytest


def test_service_info(server, data):
    '''test_service_info test the service-info API endpoint and checking if
    server is supporting the endpoint with appropriate keys in the return
    object.
    '''

    api = 'sequence/service-info'
    response = requests.get(server + api)
    assert response.status_code == 200
    service_info_object = json.loads(response.text)["service"]
    if pytest.config.getoption('--cir') is True:
        assert service_info_object["circular_supported"] == True
    else:
        assert service_info_object["circular_supported"] == False
    assert "algorithms" in service_info_object
    assert "subsequence_limit" in service_info_object
    assert "supported_api_versions" in service_info_object
