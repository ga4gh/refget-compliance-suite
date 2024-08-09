"""Module unittests.test_info_algorithms.py
This module contains methods to test the info_algorithms module via pytest.
It uses good_mock_server to validate the positive test cases 
and bad_mock_server for the negative test cases.
"""
from compliance_suite.info_algorithms import *
from compliance_suite.test_runner import TestRunner
from compliance_suite.tests import Test
from unittests.constants import GOOD_SERVER_V1_URL as good_mock_server_v1, BAD_SERVER_V1_URL as bad_mock_server_v1
from unittests.runners import good_runner_v1, bad_runner_v1, good_runner_v2, bad_runner_v2


def testing_info_algorithms():
    pass
test = Test(testing_info_algorithms)

def test_info_implement():
    info_implement(test, good_runner_v1)
    assert test.result == 1
    test.result = 2

    info_implement(test, bad_runner_v1)
    assert test.result == -1
    test.result = 2

def test_info_implement_default():
    info_implement_default(test, good_runner_v1)
    assert test.result == 1
    test.result = 2

    info_implement_default(test, bad_runner_v1)
    assert test.result == -1
    test.result = 2

def test_info_circular():
    info_circular(test, good_runner_v1)
    assert test.result == 1
    test.result = 2

    info_circular(test, bad_runner_v1)
    assert test.result == -1
    test.result = 2

def test_info_algorithms():
    info_algorithms(test, good_runner_v1)
    assert test.result == 1
    test.result = 2

    info_algorithms(test, bad_runner_v1)
    assert test.result == -1
    test.result = 2

def test_info_subsequence():
    info_subsequence(test, good_runner_v1)
    assert test.result == 1
    test.result = 2

    info_subsequence(test, bad_runner_v1)
    assert test.result == -1
    test.result = 2


def test_info_api_version():
    info_api_version(test, good_runner_v1)
    assert test.result == 1
    test.result = 2

    info_api_version(test, good_runner_v2)
    assert test.result == 0
    test.result = 2

    info_api_version(test, bad_runner_v1)
    assert test.result == -1
    test.result = 2

    info_api_version(test, bad_runner_v2)
    assert test.result == 0
    test.result = 2
