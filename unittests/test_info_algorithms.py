"""Module unittests.test_info_algorithms.py
This module contains methods to test the info_algorithms module via pytest.
"""
import pytest
import json
import click
from click.testing import CliRunner
from unittests.methods import *
from compliance_suite.info_algorithms import *
from compliance_suite.test_runner import TestRunner
from compliance_suite.tests import Test
from unittests.constants import GOOD_SERVER_URL as good_mock_server
from unittests.constants import BAD_SERVER_URL as bad_mock_server

good_runner = TestRunner(good_mock_server)
bad_runner = TestRunner(bad_mock_server)
def testing_info_algorithms():
    pass
test = Test(testing_info_algorithms)

def test_info_implement():
    info_implement(test, good_runner)
    assert test.result == 1
    test.result = 2

    info_implement(test, bad_runner)
    assert test.result == -1
    test.result = 2

def test_info_implement_default():
    info_implement_default(test, good_runner)
    assert test.result == 1
    test.result = 2

    info_implement_default(test, bad_runner)
    assert test.result == -1
    test.result = 2

def test_info_circular():
    info_circular(test, good_runner)
    assert test.result == 1
    test.result = 2

    info_circular(test, bad_runner)
    assert test.result == -1
    test.result = 2

def test_info_algorithms():
    info_algorithms(test, good_runner)
    assert test.result == 1
    test.result = 2

    info_algorithms(test, bad_runner)
    assert test.result == -1
    test.result = 2

def test_info_subsequence():
    info_subsequence(test, good_runner)
    assert test.result == 1
    test.result = 2

    info_subsequence(test, bad_runner)
    assert test.result == -1
    test.result = 2

def test_info_api_version():
    info_api_version(test, good_runner)
    assert test.result == 1
    test.result = 2

    info_api_version(test, bad_runner)
    assert test.result == -1
    test.result = 2