from algorithms import *


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
        return self.name

    def set_pass_text(self, text):
        self.pass_text = text

    def set_fail_text(self, text):
        self.fail_text = text

    def set_skip_text(self, text):
        self.skip_text = text

    def add_parent(self, parent_test_case):
        self.parents.append(parent_test_case)

    def add_child(self, child_test_case):
        self.children.append(child_test_case)
        child_test_case.add_parent(self)

    def toskip(skip_algorithm, session_params):
        pass

    def run(self, test_runner):
        self.algorithm(self, test_runner)

    def toecho(self):
        pass


def initiate_tests():
    test_base = Test(base_algorithm)

    test_info_implement = Test(info_implement)
    test_info_implement.set_pass_text('Info endpoint implemented by the server')
    test_info_implement.set_fail_text('Info endpoint not implemented by the server')

    test_info_implement_default = Test(info_implement_default)
    test_info_implement_default.set_pass_text('Info endpoint implemented with default encoding')
    test_info_implement_default.set_fail_text('Info endpoint not implemented with default encoding')

    test_info_circular = Test(info_circular)
    test_info_circular.set_pass_text('"circular" key in info response object')
    test_info_circular.set_fail_text('"circular" key not in info response object')

    test_info_algorithms = Test(info_algorithms)
    test_info_algorithms.set_pass_text('"algorithms" key in info response object')
    test_info_algorithms.set_fail_text('"algorithms" key not in info response object')

    test_info_subsequence_limit = Test(info_subsequence)
    test_info_subsequence_limit.set_pass_text('"subsequence_limit" key in info response object')
    test_info_subsequence_limit.set_pass_text('"subsequence_limit" key not in info response object')

    test_info_api_version = Test(info_api_version)
    test_info_api_version.set_pass_text('"supported_api_versions" key in info response object')
    test_info_api_version.set_pass_text('"supported_api_versions" key not in info response object')

    test_base.add_child(test_info_implement)

    test_info_implement.add_child(test_info_implement_default)
    test_info_implement.add_child(test_info_circular)
    test_info_implement.add_child(test_info_algorithms)
    test_info_implement.add_child(test_info_subsequence_limit)
    test_info_implement.add_child(test_info_api_version)

    return test_base
