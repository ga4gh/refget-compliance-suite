from info_algorithms import *
from metadata_algorithms import *


class Test():
    def __init__(self, algorithm):
        self.label = 0
        self.algorithm = algorithm
        self.result = 2
        self.pass_text = ''
        self.fail_text = ''
        self.skip_text = ''
        self.parents = []
        self.children = []

    def __str__(self):
        return 'test_' + self.algorithm.__name__

    def set_pass_text(self, text):
        self.pass_text = text

    def set_fail_text(self, text):
        self.fail_text = text

    def set_skip_text(self, text):
        self.skip_text = text

    def generate_skip_text(self):
        text = str(self) + ' is skipped because' + '\n'
        for test in self.parents:
            if test.result != 1:
                text = text + test.toecho()
        return text

    def add_parent(self, parent_test_case):
        self.parents.append(parent_test_case)

    def add_child(self, child_test_case):
        self.children.append(child_test_case)
        child_test_case.add_parent(self)

    def toskip(self):
        for test in self.parents:
            if test.result != 1:
                return True
        return False

    def run(self, test_runner):
        if self.toskip() is True:
            self.result = 0
            return
        self.algorithm(self, test_runner)

    def toecho(self):
        if self.result == 1:
            return self.pass_text
        elif self.result == -1:
            return self.fail_text
        elif self.skip_text == '':
                self.skip_text = self.generate_skip_text()
        return self.skip_text


def initiate_tests():

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
    test_info_circular.set_pass_text('"circular" key in info response object')
    test_info_circular.set_fail_text('"circular" key not in info response object instead sends ')

    test_info_algorithms = Test(info_algorithms)
    test_info_algorithms.set_pass_text('"algorithms" key in info response object')
    test_info_algorithms.set_fail_text('"algorithms" key not in info response object instead sends ')

    test_info_subsequence_limit = Test(info_subsequence)
    test_info_subsequence_limit.set_pass_text('"subsequence_limit" key in info response object')
    test_info_subsequence_limit.set_fail_text('"subsequence_limit" key not in info response object instead sends ')

    test_info_api_version = Test(info_api_version)
    test_info_api_version.set_pass_text('"supported_api_versions" key in info response object')
    test_info_api_version.set_fail_text('"supported_api_versions" key not in info response object instead sends ')

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
    test_metadata_query_circular_sequence.set_pass_text('Circular sequence metadata can be retrived')
    test_metadata_query_circular_sequence.set_fail_text('Circular sequence metadata can not be retrived even though info endpoint indicates it"s support')

    test_metadata_md5 = Test(metadata_md5)
    test_metadata_md5.set_pass_text('"md5" key in metadata response object')
    test_metadata_md5.set_fail_text('"md5" key not in metadata response object instead sends ')

    test_metadata_trunc512 = Test(metadata_trunc512)
    test_metadata_trunc512.set_pass_text('"trunc512" key in metadata response object')
    test_metadata_trunc512.set_fail_text('"trunc512" key not in metadata response object even though info endpoint indicates it"s support instead sends ')

    test_metadata_length = Test(metadata_length)
    test_metadata_length.set_pass_text('"length" key in metadata response object')
    test_metadata_length.set_fail_text('"length" key not in metadata response object or incorrect value in "length" key instead sends ')

    test_metadata_aliases = Test(metadata_aliases)
    test_metadata_aliases.set_pass_text('"aliases" key in metadata response object')
    test_metadata_aliases.set_fail_text('"aliases" key not in metadata response object')

    test_metadata_invalid_checksum_404_error = Test(metadata_invalid_checksum_404_error)
    test_metadata_invalid_checksum_404_error.set_pass_text('Server is correctly sending 404 on invalid checksum')
    test_metadata_invalid_checksum_404_error.set_fail_text('Server is not sending 404 on invalid checksum instead sends ')

    test_metadata_invalid_encoding_415_error = Test(metadata_invalid_encoding_415_error)
    test_metadata_invalid_encoding_415_error.set_pass_text('Server is correctly sending 415 on invalid encoding')
    test_metadata_invalid_encoding_415_error.set_fail_text('Server is not sending 415 on invalid encoding instead sends ')

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
    test_sequence_invalid_checksum_404_error.set_pass_text('Server is not sending 404 on invalid checksum instead sends ')

    test_sequence_invalid_encoding_415_error = Test(sequence_invalid_encoding_415_error)
    test_sequence_invalid_encoding_415_error.set_pass_text('Server is correctly sending 415 on invalid encoding')
    test_sequence_invalid_encoding_415_error.set_pass_text('Server is not sending 415 on invalid encoding instead sends ')

    test_sequence_start_end = Test(sequence_start_end)
    test_sequence_start_end.set_pass_text('Server supports start end query params')
    test_sequence_start_end.set_fail_text('Server does not support start end query params')

    test_sequence_range = Test(sequence_range)
    test_sequence_range.set_pass_text('Server supports range header')
    test_sequence_range.set_fail_text('Server does not support range header')

    test_sequence_circular = Test(sequence_circular)
    test_sequence_circular.set_pass_text('Circular sequence can be rertieved successfully')
    test_sequence_circular.set_fail_text('Circular sequences can not be retreived even though info endpoint indicates its support')


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
    test_metadata_implement.add_child(test_metadata_invalid_encoding_415_error)

    return test_base
