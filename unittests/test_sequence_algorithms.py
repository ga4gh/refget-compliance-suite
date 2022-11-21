"""Module unittests.test_sequence_algorithms.py
This module contains methods to test the sequence_algorithms module via pytest.
It uses good_mock_server to validate the positive test cases 
and bad_mock_server for the negative test cases.
"""
from compliance_suite.sequence_algorithms import sequence_implement, sequence_implement_default, \
    sequence_query_by_trunc512, sequence_invalid_checksum_404_error, sequence_invalid_encoding_406_error, \
    sequence_start_end, sequence_start_end_success_cases, sequence_range, sequence_range_success_cases, \
    sequence_circular, sequence_start_end_errors, sequence_range_errors, sequence_circular_support_true_errors, \
    sequence_circular_support_false_errors, sequence_query_by_ga4gh, sequence_query_by_insdc
from compliance_suite.test_runner import TestRunner
from compliance_suite.tests import Test
from unittests.constants import GOOD_SERVER_V1_URL as good_mock_server_v1, \
    BAD_SERVER_V1_URL as bad_mock_server_v1, \
    GOOD_SERVER_V2_URL as good_mock_server_v2, \
    BAD_SERVER_V2_URL as bad_mock_server_v2

good_runner_v1 = TestRunner(good_mock_server_v1)
good_runner_v1.session_params = {
    "limit": 400000,
    "algorithms:trunc512": True,
    "circular_supported": True,
    "redirection": None
}
bad_runner_v1 = TestRunner(bad_mock_server_v1)
bad_runner_v1.session_params = {
    "limit": 400000,
    "algorithms:trunc512": True,
    "circular_supported": True,
    "redirection": None
}
good_runner_v2 = TestRunner(good_mock_server_v2)
good_runner_v2.session_params = {
    "limit": 400000,
    "algorithms:trunc512": False,
    "algorithms:ga4gh": True,
    "identifier_types:insdc": True,
    "circular_supported": True,
    "redirection": None
}
bad_runner_v2 = TestRunner(bad_mock_server_v2)
bad_runner_v2.session_params = {
    "limit": 400000,
    "algorithms:trunc512": False,
    "algorithms:ga4gh": True,
    "identifier_types:insdc": True,
    "circular_supported": True,
    "redirection": None
}

def testing_sequence_algorithms():
    pass

test = Test(testing_sequence_algorithms)

def test_sequence_implement():
    test.result = 2
    sequence_implement(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    sequence_implement(test, bad_runner_v1)
    assert test.result == -1

def test_sequence_implement_default():
    test.result = 2
    sequence_implement_default(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    sequence_implement_default(test, bad_runner_v1)
    assert test.result == -1


def test_sequence_query_by_trunc512():
    test.result = 2
    sequence_query_by_trunc512(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    sequence_query_by_trunc512(test, bad_runner_v1)
    assert test.result == -1
    

def test_sequence_invalid_checksum_404_error():
    test.result = 2
    sequence_invalid_checksum_404_error(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    sequence_invalid_checksum_404_error(test, bad_runner_v1)
    assert test.result == -1

def test_sequence_invalid_encoding_406_error():
    test.result = 2
    sequence_invalid_encoding_406_error(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    sequence_invalid_encoding_406_error(test, bad_runner_v1)
    assert test.result == -1
    
def test_sequence_start_end():
    test.result = 2
    sequence_start_end(test, good_runner_v1)
    assert test.result == 1

    test.result = 2
    sequence_start_end(test, bad_runner_v1)
    assert test.result == -1
    
def test_sequence_start_end_success_cases():
    test.result = 2
    test.case_outputs = []
    test.cases = [
        (['?start=10&end=10', 10, 10], 0),
        (['?start=10&end=20', 10, 20], 10),
        (['?start=10&end=11', 10, 11], 1),
        (['?start=230208', 230208, None], 10),
        (['?end=5', None, 5], 5),
        (['?start=230217&end=230218', 230217, 230218], 1),
        (['?start=0', 0, None], 230218),
        (['?&end=230218', None, 230218], 230218),
        (['?start=0&end=230218', 0, 230218], 230218),
        (['?start=1&end=230218', 1, 230218], 230217),
        (['?start=230217', 230217, None], 1),
        (['?end=0', None, 0], 0)
    ]
    sequence_start_end_success_cases(test, good_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == 1

    test.result = 2
    test.case_outputs = []
    sequence_start_end_success_cases(test, bad_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == -1
    
def test_sequence_range():
    test.result = 2
    sequence_range(test, good_runner_v1)
    assert test.result == 1 

    test.result = 2
    sequence_range(test, bad_runner_v1)
    assert test.result == -1  

def test_sequence_range_success_cases():
    test.result = 2
    test.case_outputs = []
    test.cases = [
        (['bytes=10-19', 10, 19], [206, 10]),
        (['bytes=10-230217', 10, 230217], [206, 230208]),
        (['bytes=10-999999', 10, 999999], [206, 230208]),
        (['bytes=0-230217', 0, 230217], [206, 230218]),
        (['bytes=0-999999', 0, 999999], [206, 230218]),
        (['bytes=0-0', 0, 0], [206, 1]),
        (['bytes=230217-230217', 230217, 230217], [206, 1])
    ]
    sequence_range_success_cases(test, good_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == 1

    test.result = 2
    test.case_outputs = []
    sequence_range_success_cases(test, bad_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == -1

def test_sequence_circular():
    test.result = 2
    test.case_outputs = []
    test.cases = [
        ('?start=5374&end=5', ['ATCCAACCTGCAGAGTT', 17]),
        ('?start=5374&end=0', ['ATCCAACCTGCA', 12]),
        ('?start=5380&end=25', ['CCTGCAGAGTTTTATCGCTTCCATGACGCAG', 31]),
    ]
    sequence_circular(test, good_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == 1 

    test.result = 2
    test.case_outputs = []
    sequence_circular(test, bad_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == -1 

def test_sequence_start_end_errors():
    test.result = 2
    test.case_outputs = []
    test.cases = [
        (['6681ac2f62509cfc220d78751b8dc524', '?start=abc&end=20'], 400),
        (['6681ac2f62509cfc220d78751b8dc524', '?start=-10&end=-29', {}], 400),
        (['6681ac2f62509cfc220d78751b8dc524', '?start=abc'], 400),

        # Range out of bounds. Size of the sequence being tested is 5386.
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=67&end=5387'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5375'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5386'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5'], 416),
    ]
    sequence_start_end_errors(test, good_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == 1

    test.result = 2
    test.case_outputs = []
    sequence_start_end_errors(test, bad_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == -1


def test_sequence_range_errors():
    test.result = 2
    test.case_outputs = []
    test.cases = [
        (['6681ac2f62509cfc220d78751b8dc524', 'units=20-30'], 400),
        (['6681ac2f62509cfc220d78751b8dc524', 'bytes=ab-19'], 400),
        (['6681ac2f62509cfc220d78751b8dc524', 'bytes=-10--19'], 400),
        (['6681ac2f62509cfc220d78751b8dc524', 'bytes=10--19'], 400),
        (['6681ac2f62509cfc220d78751b8dc524', 'bytes=-10-'], 400),
        (['6681ac2f62509cfc220d78751b8dc524', 'bytes==10-19'], 400),

        # Range out of bounds as fbs > lbs which is not allowed
        (['3332ed720ac7eaa9b3655c06f6b9e196', 'bytes=5200-19'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', 'bytes=59-50'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', 'bytes=5385-5382'], 416),

        # Range out of bounds. Size of the sequence tested is 5386
        (['3332ed720ac7eaa9b3655c06f6b9e196', 'bytes=5387-5391'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', 'bytes=5386-5387'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', 'bytes=9999-99999'], 416)
    ]
    sequence_range_errors(test, good_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == 1

    test.result = 2
    test.case_outputs = []
    sequence_range_errors(test, bad_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        assert case_output["result"] == -1

def test_sequence_circular_support_true_errors():
    test.case_outputs = []
    test.result = 2
    test.cases = [
        (['6681ac2f62509cfc220d78751b8dc524', '?start=220218&end=671'], 416)
    ]
    # if circular support in session params is False, then the test is skipped
    good_runner_v1.session_params["circular_supported"]= False
    sequence_circular_support_true_errors(test, good_runner_v1)
    assert test.result == 0

    # if circular support in session params is True
    good_runner_v1.session_params["circular_supported"]= True
    test.case_outputs =[]
    test.result = 2
    sequence_circular_support_true_errors(test, good_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        # good_mock_server supports circular sequences. 
        # the status code != 501 as expected
        assert case_output["result"] == 1


    test.case_outputs = []
    test.result = 2
    sequence_circular_support_true_errors(test, bad_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        # bad_mock_server supports circular sequences. 
        # It provides incorrect error codes
        assert case_output["result"] == -1

def test_sequence_circular_support_false_errors():
    test.case_outputs = []
    test.result = 2
    test.cases = [
        (['6681ac2f62509cfc220d78751b8dc524', '?start=220218&end=671'], 501),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=20&end=4'], 501)
    ]

    # if circular support in session params is True, then the test is skipped
    good_runner_v1.session_params["circular_supported"]= True
    sequence_circular_support_false_errors(test, good_runner_v1)
    assert test.result == 0
    
    # if circular support in session params is False
    good_runner_v1.session_params["circular_supported"]=False
    test.result = 2
    test.case_outputs = []
    sequence_circular_support_false_errors(test, good_runner_v1)
    assert len(test.case_outputs) == len(test.cases)
    for case_output in test.case_outputs:
        # good_mock_server supports circular sequences. 
        # the status code != 501 as expected
        assert case_output["result"] == -1 

    test.case_outputs = []
    test.result = 2
    sequence_circular_support_false_errors(test, bad_runner_v1)
    # bad_mock_server supports circular sequence. It also provides incorrect error codes
    for case_output in test.case_outputs:
        assert case_output["result"] == -1


def test_sequence_query_by_ga4gh():
    test.result = 2
    sequence_query_by_ga4gh(test, good_runner_v2)
    assert test.result == 1

    test.result = 2
    sequence_query_by_ga4gh(test, bad_runner_v2)
    assert test.result == -1


def test_sequence_query_by_insdc():
    test.result = 2
    sequence_query_by_insdc(test, good_runner_v2)
    assert test.result == 1

    test.result = 2
    sequence_query_by_insdc(test, bad_runner_v2)
    assert test.result == -1
