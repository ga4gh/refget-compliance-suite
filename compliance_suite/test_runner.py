from compliance_suite.tests import initiate_tests
from compliance_suite.utils import data
import datetime
import re
import sys


def processed_func_descrp(text):
    return re.sub(' +', ' ', text.replace('\n', '')).strip()


class TestRunner():
    '''
    Test runner class used to run tests, pass context variables through test
    graph to generate report appropriately.
    '''
    def __init__(self, base_url):
        '''
        Required params:
            base_url - The base url of the server on which the report will be
                generated

        Object params:
            session_params - Variables from info endpoint used to run conditional
                tests. Values are populated when info endpoint tests are run
            total_tests - Total number of tests
            total_tests_passed - Total number of tests passed
            total_tests_failed - Total number of tests failed
            total_tests_skipped - Total number of tests skipped
            total_tests_warning - Total number of tests generated warning
            results - To store test result objects for report generation
        '''

        self.root = None
        self.session_params = {
            'limit': None,
            'trunc512': None,
            'circular': None,
            'redirection': None
        }
        self.test_data = data()
        self.total_tests = 0
        self.total_tests_passed = 0
        self.total_tests_skipped = 0
        self.total_tests_failed = 0
        self.total_tests_warning = 0
        self.base_url = base_url
        self.results = []

    def recurse_label_tests(self, root):
        '''
        Labels the test case nodes and populate label parameter in test objects.
        to ensure parents are run first no matter the shape of test graph
        '''
        label = root.label + 1
        for child in root.children:
            if label > child.label:
                self.total_tests = self.total_tests + 1
                child.label = label
            if len(child.children) != 0:
                self.recurse_label_tests(child)

    def recurse_generate_json(self, node):
        '''
        Generate the report according to the label set in above function by
        test_result_object s. It also populates other params of test_runner
        object
        '''
        label = node.label + 1
        for child in node.children:
            if child.label == label:
                test_result_object = {
                    'name': str(child),
                    'result': child.result,
                    'test_description': processed_func_descrp(child.algorithm.__doc__),
                    'text': child.to_echo(),
                    'parents': [str(parent) for parent in child.parents],
                    'children': [str(child) for child in child.children],
                    'warning': child.warning,
                    'edge_cases': child.case_outputs,
                    # 'edge_cases': [case for case in child.case_outputs if case['result'] == -1]
                }
                if child.result == 1:
                    self.total_tests_passed = self.total_tests_passed + 1
                elif child.result == -1:
                    self.total_tests_failed = self.total_tests_failed + 1
                else:
                    self.total_tests_skipped = self.total_tests_skipped + 1
                if child.warning is True:
                    self.total_tests_warning = self.total_tests_warning + 1
                self.results.append(test_result_object)
                if len(child.children) != 0:
                    self.recurse_generate_json(child)

    def recurse_run_tests(self, node):
        '''
        Runs the test graph according to the label set
        '''
        label = node.label + 1
        for child in node.children:
            if child.label == label:
                print(str(child), file=sys.stderr)
                child.run(self)
        for child in node.children:
            if len(child.children) != 0:
                self.recurse_run_tests(child)

    def generate_final_json(self):
        '''
        Generate final report object for this session
        '''
        now = datetime.datetime.now()
        report_object = {
            'server': self.base_url,
            'date_time': str(now),
            'test_results': self.results,
            'total_tests': self.total_tests,
            'total_tests_passed': self.total_tests_passed,
            'total_tests_skipped': self.total_tests_skipped,
            'total_tests_failed': self.total_tests_failed,
            'total_warnings': self.total_tests_warning
        }
        return report_object

    def run_tests(self):
        '''
        The controller function of the test runner object. Defines the
        complete pipeline.
        '''
        self.root = initiate_tests()
        self.root.run(self)
        self.recurse_label_tests(self.root)
        self.recurse_run_tests(self.root)
        self.recurse_generate_json(self.root)


if __name__ == "__main__":
    tr = TestRunner('https://www.ebi.ac.uk/ena/cram/')
    tr.run_tests()

    print('--------------', file=sys.stderr)

    # tr = TestRunner('http://localhost:5000/')
    # tr.run_tests()
