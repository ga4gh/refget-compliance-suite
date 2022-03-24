from unittest import skip
from compliance_suite.tests import initiate_tests
from compliance_suite.utils import data
import datetime
import re
import sys
import ga4gh
#from compliance_suite.info_algorithms import *
#from compliance_suite.metadata_algorithms import *
from compliance_suite.sequence_algorithms import *
from compliance_suite.tests import tests_in_phase
from ga4gh.testbed.report.report import Report
from ga4gh.testbed.report.constants import TIMESTAMP_FORMAT



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
            'circular_supported': None,
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
        self.report = Report()
        self.report.set_start_time(str(datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT)))
        self.start_time = {}
        self.end_time = {}
        self.phase_start_time = {}
        self.phase_end_time = {}
        self.hls_to_phase={'test_info_implement': 'service info', 
                      'test_metadata_implement': 'metadata', 
                      'test_sequence_implement': 'sequence', 
                      'test_sequence_range': 'sequence range'}
        self.parent_short_name={'test_info_implement': 'test_info', 
                      'test_metadata_implement': 'test_metadata', 
                      'test_sequence_implement': 'test_sequence', 
                      'test_sequence_range': 'test_sequence_range'}

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
                self.start_time[str(child)] = str(datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT))
                child.run(self)
                self.end_time[str(child)] = str(datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT))

        for child in node.children:
            if len(child.children) != 0:
                if str(child) in self.hls_to_phase:
                    self.phase_start_time[str(child)] = str(datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT))
                self.recurse_run_tests(child)
                if str(child) in self.hls_to_phase:
                    self.phase_end_time[str(child)] = str(datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT))

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

    def generate_report(self):
        '''
        Generate report object from GA4GH Testbed
        '''
        sequence_start_times = get_sequence_start_times()
        sequence_end_times = get_sequence_end_times()

        #for key, value in sequence_start_times.items():
        #    print(key, value)

        self.report.set_testbed_name("refget-compliance-suite")
        self.report.add_input_parameter('server', self.base_url)

        for high_level_name in ('test_info_implement', 'test_metadata_implement', 'test_sequence_implement', 'test_sequence_range'):

            #Create Report Phases
            phase = self.report.add_phase()
            phase.set_phase_name(self.hls_to_phase[high_level_name])
            phase.set_start_time(self.phase_start_time[high_level_name])
            phase.set_end_time(self.phase_end_time[high_level_name])

            #Create tests for phase            
            for test in self.results:

                #Checks against checks membership of tests agaist test_in_phase dict generated from tests
                if test['name'] in tests_in_phase[self.hls_to_phase[high_level_name]]:
                    ga4gh_test = phase.add_test()
                    ga4gh_test.set_test_name(test['name'])
                    ga4gh_test.set_test_description(test['test_description'])
                    ga4gh_test.set_start_time(self.start_time[test['name']])
                    ga4gh_test.set_end_time(self.end_time[test['name']])
                    ga4gh_test.set_message(test['text'])

                    #generates a base case for tests without cases to set pass status
                    if not test['edge_cases']:
                        ga4gh_test_case = ga4gh_test.add_case()
                        ga4gh_test_case.set_case_name(test['name'])
                        ga4gh_test_case.set_case_name(test['test_description'])
                        ga4gh_test_case.set_start_time(self.start_time[test['name']])
                        ga4gh_test_case.set_end_time(self.end_time[test['name']])                    

                        #set case status based on the result
                        if test['result'] == 1:
                            ga4gh_test_case.set_status_pass()
                        elif test['result'] == 0:
                            ga4gh_test_case.set_status_skip()                       
                        elif test['result'] == -1:
                            ga4gh_test_case.set_status_fail()
                        elif test['result'] == 2:
                            ga4gh_test_case.set_status_unknown()                 

                    #creates cases for test
                    for case in test['edge_cases']:
                        ga4gh_case = ga4gh_test.add_case()
                        ga4gh_case.set_case_name('API call')

                        #tries to retrieve time of test case execution
                        try:
                            ga4gh_case.set_start_time(sequence_start_times[str(case['api'])])
                            ga4gh_case.set_end_time(sequence_end_times[str(case['api'])])
                        except:
                            ga4gh_case.set_start_time(0)
                            ga4gh_case.set_end_time(0)

                        #set case status based on the result
                        if case['result'] == 1:
                            ga4gh_case.set_status_pass()
                        elif case['result'] == 0:
                            ga4gh_case.set_status_skip()
                        elif case['result'] == -1:
                            ga4gh_case.set_status_fail()
                        elif case['result'] == 2:
                            ga4gh_case.set_status_unknown()                                               
                        ga4gh_case.add_log_message('api' + ': ' + str(case['api']))

        self.report.set_end_time(str(datetime.datetime.utcnow().strftime(TIMESTAMP_FORMAT)))
        self.report.finalize()

        return self.report


if __name__ == "__main__":
    tr = TestRunner('https://www.ebi.ac.uk/ena/cram/')
    tr.run_tests()

    print('--------------', file=sys.stderr)

    # tr = TestRunner('http://localhost:5000/')
    # tr.run_tests()
