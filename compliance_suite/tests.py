from compliance_suite.info_algorithms import *
from compliance_suite.metadata_algorithms import *
from compliance_suite.sequence_algorithms import *
import sys

class Test():
    '''
    Test Case class. All the test cases are instances of this class.

    label - used in graph algorithms to label the test case graph
    algorithm - Strategy design pattern in used here. It is the underlying algorithm used in the test case
    result - 0 indicates skipped, 1 indicates passed, -1 indicates failed and 2 is not yet ran
    pass_text - text in the report when test case is passed
    skip_text - text in the report when test case is skipped
    fail_text - text in the report when test case is failed
    parents - dependencies of the test case to run
    children - test cases which have this test case as dependency
    warning - if the result of this test case is warning for the server implementation
    cases - multiple edge cases of same test object
    '''
    def __init__(self, algorithm):
        '''
        Initiates the Test Case object. Algorithm is a required field to initiate test case object
        '''
        self.label = 0
        self.algorithm = algorithm
        self.result = 2
        self.pass_text = ''
        self.fail_text = ''
        self.skip_text = ''
        self.parents = []
        self.children = []
        self.warning = False
        self.cases = []
        self.case_outputs = []

    def __str__(self):
        '''
        String repr of the test case
        '''
        return 'test_' + self.algorithm.__name__

    def set_pass_text(self, text):
        '''
        Setter for pass_text
        '''
        self.pass_text = text

    def set_fail_text(self, text):
        '''
        Setter for fail_text
        '''
        self.fail_text = text

    def set_skip_text(self, text):
        '''
        Setter for skip_text
        '''
        self.skip_text = text

    def generate_skip_text(self):
        '''
        Skip text is generated if there is no skip text (the case when test is skipped when the parent test cases fail or skip)
        To track down the root cause of this skip.
        '''
        text = str(self) + ' is skipped because '
        for test in self.parents:
            if test.result != 1:
                text = text + test.to_echo()
        return text

    def add_parent(self, parent_test_case):
        '''
        Adds a parent test case
        '''
        self.parents.append(parent_test_case)

    def add_child(self, child_test_case):
        '''
        Adds a child test case
        '''
        self.children.append(child_test_case)
        child_test_case.add_parent(self)

    def to_skip(self):
        '''
        Checks if any of the parent test cases failed or skipped which causes this case to skip
        '''
        for test in self.parents:
            if test.result != 1:
                print("{} - {}".format(str(test), str(test.result)), file=sys.stderr)
                return True
        return False

    def run(self, test_runner):
        '''
        First checks if the parent test cases were successful then run the text.
        '''
        # Checking if to skip
        if self.to_skip() is True:
            # warning will be generated because the test case is skipped because of some parent failure
            self.warning = True
            self.result = 0
            return
        # run the test if not skipped
        self.algorithm(self, test_runner)
        # if it fails it'll generate a warning
        if self.result == -1:
            self.warning = True

    def to_echo(self):
        '''
        Returns the text based on the result of the test case
        '''
        if self.result == 1:
            return self.pass_text
        elif self.result == -1:
            return self.fail_text
        elif self.result == 2:
            return 'Unknown error'
        elif self.skip_text == '':
            self.skip_text = self.generate_skip_text()
        return self.skip_text


def initiate_tests():
    '''
    Initiates test case objects and generates a test case graph for execution
    '''

    def base_algorithm(test, runner):
        if True is True:
            test.result = 1

    # Base test case
    test_base = Test(base_algorithm)

    # Info Success Test Cases

    test_info_implement = Test(info_implement)
    test_info_implement.set_pass_text('Info endpoint implemented by the server')
    test_info_implement.set_fail_text('Info endpoint not implemented by the server')

    test_info_implement_default = Test(info_implement_default)
    test_info_implement_default.set_pass_text('Info endpoint implemented with default encoding')
    test_info_implement_default.set_fail_text('Info endpoint not implemented with default encoding')

    test_info_circular = Test(info_circular)
    test_info_circular.set_pass_text('circular key in info response object')
    test_info_circular.set_fail_text('"circular" key not in info response object. It sends ')

    test_info_algorithms = Test(info_algorithms)
    test_info_algorithms.set_pass_text('algorithms key in info response object')
    test_info_algorithms.set_fail_text('"algorithms" key not in info response object. It sends ')

    test_info_subsequence_limit = Test(info_subsequence)
    test_info_subsequence_limit.set_pass_text('subsequence_limit key in info response object')
    test_info_subsequence_limit.set_fail_text('"subsequence_limit" key not in info response object. It sends ')

    test_info_api_version = Test(info_api_version)
    test_info_api_version.set_pass_text('supported_api_versions key in info response object')
    test_info_api_version.set_fail_text('supported_api_versions key not in info response object. It sends ')

    # Metadata Success Test Cases

    test_metadata_implement = Test(metadata_implement)
    test_metadata_implement.set_pass_text('Metadata endpoint implemented by the server')
    test_metadata_implement.set_fail_text('Metadata endpoint not implemented by the server')

    test_metadata_implement_default = Test(metadata_implement_default)
    test_metadata_implement_default.set_pass_text('Metadata endpoint implemented with default encoding')
    test_metadata_implement_default.set_fail_text('Metadata endpoint not implemented with default encoding')

    test_metadata_query_by_trunc512 = Test(metadata_query_by_trunc512)
    test_metadata_query_by_trunc512.set_pass_text('TRUNC512 algorithm is working in the server for metadata endpoint')
    test_metadata_query_by_trunc512.set_fail_text('TRUNC512 algorithm is not working in the server for metadata endpoint even though info endpoint indicates it"s support')

    test_metadata_query_circular_sequence = Test(metadata_query_circular_sequence)
    test_metadata_query_circular_sequence.set_pass_text('Circular sequence metadata can be retrieved')
    test_metadata_query_circular_sequence.set_fail_text('Circular sequence metadata can not be retrieved even though info endpoint indicates it"s support')

    test_metadata_md5 = Test(metadata_md5)
    test_metadata_md5.set_pass_text('md5 key in metadata response object')
    test_metadata_md5.set_fail_text('md5 key not in metadata response object instead sends ')

    test_metadata_trunc512 = Test(metadata_trunc512)
    test_metadata_trunc512.set_pass_text('trunc512 key in metadata response object')
    test_metadata_trunc512.set_fail_text('trunc512 key not in metadata response object even though info endpoint indicates it"s support instead sends ')

    test_metadata_length = Test(metadata_length)
    test_metadata_length.set_pass_text('length key in metadata response object')
    test_metadata_length.set_fail_text('length key not in metadata response object or incorrect value in "length" key instead sends ')

    test_metadata_aliases = Test(metadata_aliases)
    test_metadata_aliases.set_pass_text('aliases key in metadata response object')
    test_metadata_aliases.set_fail_text('aliases key not in metadata response object')

    test_metadata_invalid_checksum_404_error = Test(metadata_invalid_checksum_404_error)
    test_metadata_invalid_checksum_404_error.set_pass_text('Server is correctly sending 404 on invalid checksum')
    test_metadata_invalid_checksum_404_error.set_fail_text('Server is not sending 404 on invalid checksum instead sends ')

    test_metadata_invalid_encoding_406_error = Test(metadata_invalid_encoding_406_error)
    test_metadata_invalid_encoding_406_error.set_pass_text('Server is correctly sending 406 on invalid encoding')
    test_metadata_invalid_encoding_406_error.set_fail_text('Server is not sending 406 on invalid encoding instead sends ')

    # Sequence endpoint test cases

    test_sequence_implement = Test(sequence_implement)
    test_sequence_implement.set_pass_text('Sequence endpoint implemented in the server')
    test_sequence_implement.set_fail_text('Sequence endpoint not implemented in the server')

    test_sequence_implement_default = Test(sequence_implement_default)
    test_sequence_implement_default.set_pass_text('Sequence endpoint implemented with default encoding')
    test_sequence_implement_default.set_fail_text('Sequence endpoint not implemented with default encoding')

    test_sequence_query_by_trunc512 = Test(sequence_query_by_trunc512)
    test_sequence_query_by_trunc512.set_pass_text('TRUNC512 algorithm is working in the server for sequence endpoint')
    test_sequence_query_by_trunc512.set_fail_text('TRUNC512 algorithm is not working in the server for sequence endpoint even though info endpoint indicates it"s support')

    test_sequence_invalid_checksum_404_error = Test(sequence_invalid_checksum_404_error)
    test_sequence_invalid_checksum_404_error.set_pass_text('Server is correctly sending 404 on invalid checksum')
    test_sequence_invalid_checksum_404_error.set_fail_text('Server is not sending 404 on invalid checksum instead sends ')

    test_sequence_invalid_encoding_406_error = Test(sequence_invalid_encoding_406_error)
    test_sequence_invalid_encoding_406_error.set_pass_text('Server is correctly sending 406 on invalid encoding')
    test_sequence_invalid_encoding_406_error.set_fail_text('Server is not sending 406 on invalid encoding instead sends ')

    test_sequence_start_end = Test(sequence_start_end)
    test_sequence_start_end.set_pass_text('Server supports start end query params')
    test_sequence_start_end.set_fail_text('Server does not support start end query params')

    test_sequence_start_end_success_cases = Test(sequence_start_end_success_cases)
    test_sequence_start_end_success_cases.set_pass_text('Server passed all the success edge cases with start end query params')
    test_sequence_start_end_success_cases.set_fail_text('Server did not pass all the success edge cases with start end query params. Check <a href="https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/success/#sub-sequence-queries">https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/success/#sub-sequence-queries</a>')
    test_sequence_start_end_success_cases.cases = [
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

    test_sequence_range = Test(sequence_range)
    test_sequence_range.set_pass_text('Server supports range header')
    test_sequence_range.set_fail_text('Server does not support range header')

    test_sequence_range_success_cases = Test(sequence_range_success_cases)
    test_sequence_range_success_cases.set_pass_text('Server passed all the success edge cases with range header query')
    test_sequence_range_success_cases.set_fail_text('Server did not pass all the success edge cases with range header query. Check <a href="https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/success/#sub-sequence-queries">https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/success/#sub-sequence-queries</a>')
    test_sequence_range_success_cases.cases = [
        (['bytes=10-19', 10, 19], [206, 10]),
        (['bytes=10-230217', 10, 230217], [206, 230208]),
        (['bytes=10-999999', 10, 999999], [206, 230208]),
        (['bytes=0-230217', 0, 230217], [206, 230218]),
        (['bytes=0-999999', 0, 999999], [206, 230218]),
        (['bytes=0-0', 0, 0], [206, 1]),
        (['bytes=230217-230217', 230217, 230217], [206, 1])
    ]

    test_sequence_circular = Test(sequence_circular)
    test_sequence_circular.set_pass_text('Circular sequence can be retrieved successfully passing all the edge cases')
    test_sequence_circular.set_fail_text('Circular sequences can not be retrieved even though info endpoint indicates its support')
    test_sequence_circular.cases = [
        ('?start=5374&end=5', ['ATCCAACCTGCAGAGTT', 17]),
        ('?start=5374&end=0', ['ATCCAACCTGCA', 12]),
        ('?start=5380&end=25', ['CCTGCAGAGTTTTATCGCTTCCATGACGCAG', 31]),
    ]

    test_sequence_start_end_errors = Test(sequence_start_end_errors)
    test_sequence_start_end_errors.set_pass_text('Server is correctly throwing errors for start-end error cases')
    test_sequence_start_end_errors.set_fail_text('Server is not correctly throwing errors for start-end error cases. Check <a href="https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-start-end-parameters">https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-start-end-parameters</a>')
    test_sequence_start_end_errors.cases = [

        (['6681ac2f62509cfc220d78751b8dc524', '?start=abc&end=20'], 400),
        (['6681ac2f62509cfc220d78751b8dc524', '?start=-10&end=-29', {}], 400),
        (['6681ac2f62509cfc220d78751b8dc524', '?start=abc'], 400),

        # Range out of bounds. Size of the sequence being tested is 5386.
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=67&end=5387'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5375'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5386'], 416),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=5386&end=5'], 416),
    ]

    test_sequence_range_errors = Test(sequence_range_errors)
    test_sequence_range_errors.set_pass_text('Server is correctly throwing errors for range error cases')
    test_sequence_range_errors.set_fail_text('Server is not correctly throwing errors for range error cases. Check <a href="https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-range-header">https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-range-header</a>')
    test_sequence_range_errors.cases = [
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

    test_sequence_circular_support_false_errors = Test(sequence_circular_support_false_errors)
    test_sequence_circular_support_false_errors.set_pass_text('Server is correctly throwing for error cases of circular sequences when server does not support circular sequences')
    test_sequence_circular_support_false_errors.set_fail_text('Server is not correctly throwing for error cases of circular sequences when server does not support circular sequences. Check <a href="https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-start-end-parameters">https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-start-end-parameters</a>')
    test_sequence_circular_support_false_errors.cases = [
        (['6681ac2f62509cfc220d78751b8dc524', '?start=220218&end=671'], 501),
        (['3332ed720ac7eaa9b3655c06f6b9e196', '?start=20&end=4'], 501)
    ]

    test_sequence_circular_support_true_errors = Test(sequence_circular_support_true_errors)
    test_sequence_circular_support_true_errors.set_pass_text('Server is correctly throwing for error cases of circular sequences when server supports circular sequences')
    test_sequence_circular_support_true_errors.set_fail_text('Server is not correctly throwing for error cases of circular sequences when server supports circular sequences. Check <a href="https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-start-end-parameters">https://compliancedoc.readthedocs.io/en/latest/GET_sequence_API/errors/#error-conditions-while-using-start-end-parameters</a>')
    test_sequence_circular_support_true_errors.cases = [
        (['6681ac2f62509cfc220d78751b8dc524', '?start=220218&end=671'], 416)
    ]

    # generating test graph

    test_base.add_child(test_info_implement)

    test_info_implement.add_child(test_info_implement_default)
    test_info_implement.add_child(test_info_circular)
    test_info_implement.add_child(test_info_algorithms)
    test_info_implement.add_child(test_info_subsequence_limit)
    test_info_implement.add_child(test_info_api_version)

    test_base.add_child(test_metadata_implement)

    test_metadata_implement.add_child(test_metadata_implement_default)

    test_metadata_implement.add_child(test_metadata_query_by_trunc512)
    test_info_algorithms.add_child(test_metadata_query_by_trunc512)

    test_metadata_implement.add_child(test_metadata_query_circular_sequence)
    test_info_circular.add_child(test_metadata_query_circular_sequence)

    test_metadata_implement.add_child(test_metadata_md5)

    test_metadata_implement.add_child(test_metadata_trunc512)
    test_info_algorithms.add_child(test_metadata_trunc512)

    test_metadata_implement.add_child(test_metadata_length)
    test_metadata_implement.add_child(test_metadata_aliases)
    test_metadata_implement.add_child(test_metadata_invalid_checksum_404_error)
    test_metadata_implement.add_child(test_metadata_invalid_encoding_406_error)

    test_base.add_child(test_sequence_implement)

    test_sequence_implement.add_child(test_sequence_implement_default)
    test_sequence_implement.add_child(test_sequence_start_end)
    test_sequence_implement.add_child(test_sequence_range)

    test_sequence_implement.add_child(test_sequence_query_by_trunc512)
    test_info_algorithms.add_child(test_sequence_query_by_trunc512)

    test_sequence_implement.add_child(test_sequence_invalid_checksum_404_error)

    test_sequence_implement.add_child(test_sequence_invalid_encoding_406_error)

    test_sequence_start_end.add_child(test_sequence_start_end_success_cases)
    test_sequence_range.add_child(test_sequence_range_success_cases)

    test_sequence_implement.add_child(test_sequence_circular)
    test_info_circular.add_child(test_sequence_circular)

    test_sequence_start_end.add_child(test_sequence_start_end_errors)

    test_sequence_range.add_child(test_sequence_range_errors)

    test_sequence_implement.add_child(test_sequence_circular_support_false_errors)
    test_info_circular.add_child(test_sequence_circular_support_false_errors)

    test_sequence_implement.add_child(test_sequence_circular_support_true_errors)
    test_info_circular.add_child(test_sequence_circular_support_true_errors)

    return test_base
