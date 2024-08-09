"""Module unittests.test_metadata_algorithms.py
This module contains methods to test the metadata_algorithms module via pytest.
It uses good_mock_server to validate the positive test cases 
and bad_mock_server for the negative test cases.
"""
from compliance_suite.metadata_algorithms import metadata_implement, metadata_implement_default, \
    metadata_query_by_trunc512, metadata_query_circular_sequence, metadata_md5, metadata_trunc512, metadata_length, \
    metadata_aliases, metadata_invalid_encoding_406_error, \
    metadata_query_by_ga4gh, metadata_query_by_insdc, metadata_invalid_checksum_404_error
from compliance_suite.test_runner import TestRunner
from compliance_suite.tests import Test
import unittests.constants
from unittests.runners import good_runner_v1, bad_runner_v1, good_runner_v2, bad_runner_v2


def testing_metadata_algorithms():
    pass
test = Test(testing_metadata_algorithms)


def test_metadata_implement():
    test.result = 2
    metadata_implement(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    metadata_implement(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_implement_default():
    test.result = 2
    metadata_implement_default(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    metadata_implement_default(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_query_by_trunc512():
    test.result = 2
    metadata_query_by_trunc512(test, good_runner_v1)
    assert test.result == 1

    # if trunc512 is not supported
    test.result = 2
    good_runner_v1.session_params["algorithms:trunc512"] = False
    metadata_query_by_trunc512(test, good_runner_v1)
    assert test.result == 0

    test.result = 2
    metadata_query_by_trunc512(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_query_circular_sequence():
    test.result = 2
    metadata_query_circular_sequence(test, good_runner_v1)
    assert test.result == 1

    # is circular_support is False
    test.result = 2
    good_runner_v1.session_params["circular_supported"]= False
    metadata_query_circular_sequence(test, good_runner_v1)
    assert test.result == 0

    test.result = 2
    metadata_query_circular_sequence(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_md5():
    test.result = 2
    metadata_md5(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    metadata_md5(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_trunc512():

    # if trunc512 is supported
    test.result = 2
    good_runner_v1.session_params["algorithms:trunc512"] = True
    metadata_trunc512(test, good_runner_v1)
    assert test.result == 1

    # if trunc512 is not supported
    test.result = 2
    good_runner_v1.session_params ["algorithms:trunc512"]= False
    metadata_query_by_trunc512(test, good_runner_v1)
    assert test.result == 0

    # if trunc512 is supported
    test.result = 2
    good_runner_v1.session_params["algorithms:trunc512"] = True
    metadata_trunc512(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_length():
    test.result = 2
    metadata_length(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    metadata_length(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_aliases():
    test.result = 2
    metadata_aliases(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    metadata_aliases(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_invalid_checksum_404_error():
    test.result = 2
    metadata_invalid_checksum_404_error(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    metadata_invalid_checksum_404_error(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_invalid_encoding_406_error():
    test.result = 2
    metadata_invalid_encoding_406_error(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    metadata_invalid_encoding_406_error(test, bad_runner_v1)
    assert test.result == -1


def test_metadata_query_by_ga4gh():
    test.result = 2
    metadata_query_by_ga4gh(test, good_runner_v2)
    assert test.result == 1

    test.result = 2
    metadata_query_by_ga4gh(test, bad_runner_v2)
    assert test.result == -1


def test_sequence_query_by_insdc():
    test.result = 2
    metadata_query_by_insdc(test, good_runner_v2)
    assert test.result == 1

    test.result = 2
    metadata_query_by_insdc(test, bad_runner_v2)
    assert test.result == -1
