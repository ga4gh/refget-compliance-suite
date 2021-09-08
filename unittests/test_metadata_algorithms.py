"""Module unittests.test_metadata_algorithms.py
This module contains methods to test the metadata_algorithms module via pytest.
"""
import pytest
import json
import click
from click.testing import CliRunner
from unittests.methods import *
from compliance_suite.metadata_algorithms import *
from compliance_suite.test_runner import TestRunner
from compliance_suite.tests import Test
from unittests.constants import GOOD_SERVER_URL as good_mock_server
from unittests.constants import BAD_SERVER_URL as bad_mock_server

good_runner = TestRunner(good_mock_server)
good_runner.session_params = {
    "limit": 400000,
    "trunc512": True,
    "circular_supported": None,
    "redirection": None
        }
bad_runner = TestRunner(bad_mock_server)
bad_runner.session_params = {
    "limit": 400000,
    "trunc512": True,
    "circular_supported": None,
    "redirection": None
        }
def testing_metadata_algorithms():
    pass
test = Test(testing_metadata_algorithms)

def test_metadata_implement():
    test.result = 2
    metadata_implement(test, good_runner)
    assert test.result == 1

    test.result = 2
    metadata_implement(test, bad_runner)
    assert test.result == -1

def test_metadata_implement_default():
    test.result = 2
    metadata_implement_default(test, good_runner)
    assert test.result == 1

    test.result = 2
    metadata_implement_default(test, bad_runner)
    assert test.result == -1
    
def test_metadata_query_by_trunc512():
    test.result = 2
    metadata_query_by_trunc512(test, good_runner)
    assert test.result == 1

    # if trunc512 is not supported
    test.result = 2
    good_runner.session_params = {
        "limit": 400000,
        "trunc512": False,
        "circular_supported": None,
        "redirection": None
            }
    metadata_query_by_trunc512(test, good_runner)
    assert test.result == 0

    test.result = 2
    metadata_query_by_trunc512(test, bad_runner)
    assert test.result == -1

def test_metadata_query_circular_sequence():
    test.result = 2
    metadata_query_circular_sequence(test, good_runner)
    assert test.result == 1

    # is circular_support is False
    test.result = 2
    good_runner.session_params = {
        "limit": 400000,
        "trunc512": None,
        "circular_supported": False,
        "redirection": None
            }
    metadata_query_circular_sequence(test, good_runner)
    assert test.result == 0

    test.result = 2
    metadata_query_circular_sequence(test, bad_runner)
    assert test.result == -1

def test_metadata_md5():
    test.result = 2
    metadata_md5(test, good_runner)
    assert test.result == 1

    test.result = 2
    metadata_md5(test, bad_runner)
    assert test.result == -1

def test_metadata_trunc512():

    # if trunc512 is supported
    test.result = 2
    good_runner.session_params = {
        "limit": 400000,
        "trunc512": True,
        "circular_supported": None,
        "redirection": None
            }
    metadata_trunc512(test, good_runner)
    assert test.result == 1

    # if trunc512 is not supported
    test.result = 2
    good_runner.session_params = {
        "limit": 400000,
        "trunc512": False,
        "circular_supported": None,
        "redirection": None
            }
    metadata_query_by_trunc512(test, good_runner)
    assert test.result == 0

    test.result = 2
    good_runner.session_params = {
        "limit": 400000,
        "trunc512": True,
        "circular_supported": None,
        "redirection": None
            }
    metadata_trunc512(test, bad_runner)
    assert test.result == -1

def test_metadata_length():
    test.result = 2
    metadata_length(test, good_runner)
    assert test.result == 1

    test.result = 2
    metadata_length(test, bad_runner)
    assert test.result == -1

def test_metadata_aliases():
    test.result = 2
    metadata_aliases(test, good_runner)
    assert test.result == 1

    test.result = 2
    metadata_aliases(test, bad_runner)
    assert test.result == -1

def test_metadata_invalid_checksum_404_error():
    test.result = 2
    metadata_invalid_checksum_404_error(test, good_runner)
    assert test.result == 1

    test.result = 2
    metadata_invalid_checksum_404_error(test, bad_runner)
    assert test.result == -1

def test_metadata_invalid_encoding_406_error():
    test.result = 2
    metadata_invalid_encoding_406_error(test, good_runner)
    assert test.result == 1

    test.result = 2
    metadata_invalid_encoding_406_error(test, bad_runner)
    assert test.result == -1