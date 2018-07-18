tests = [
    'info_implementation'
    'info_default_encoding',
    'info_content_type',
    'info_circular',
    'info_subsequence_limit',
    'info_alorithms',
    'info_api_version',

    'metadata_implementation',
    'metadata_default_encoding',
    'metadata_md5',
    'metadata_trunc512',
    'metadata_length',
    'metadata_aliases'
    'metadata_trunc512',
    'metadata_content_type',
    'metadata_invalid_checksum_404_error'
]

TEST_STATE_PARAMS = {
    'info_implement': None,
    'metadata_implement': None,
    'limit': None,
    'trunc512': None,
    'circular': None,
    'redirection': None
}

TEST_RESULTS = [
    # {'info_status_code': [0, 'failure_reason']},
]


def test_service_info(params, server, data):
    api = 'sequence/service-info'
    response = requests.get(server + api)
    assert response.status_code == 200
    service_info_object = json.loads(response.text)["service"]

    assert "algorithms" in service_info_object
    assert "subsequence_limit" in service_info_object
    assert "supported_api_versions" in service_info_object


def main():
    # test_service_info(TEST_STATE_PARAMS, TEST_RESULTS)
    # echo_report(TEST_RESULTS)
    pass


if __name__ == "__main__":
    main()
