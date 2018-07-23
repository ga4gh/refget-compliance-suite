from tests import initiate_tests


class TestRunner():
    def __init__(self, base_url):
        self.root = None
        self.session_params = {
            'limit': None,
            'trunc512': None,
            'circular': None,
            'redirection': None
        }
        self.total_tests = 0
        self.total_tests_passed = 0
        self.total_tests_skipped = 0
        self.total_tests_failed = 0
        self.base_url = base_url

    def recurse_label_tests(self, root):
        label = root.label + 1
        for child in root.children:
            if label > child.label:
                self.total_tests = self.total_tests + 1
                child.label = label
            if len(child.children) != 0:
                self.recurse_label_tests(child)

    def generate_report(self, node):
        label = node.label + 1
        for child in node.children:
            if child.label == label:
                print('.')
                if child.result == 1:
                    print('PASSED: ' + str(child))
                elif child.result == -1:
                    print('FAILED: ' + str(child))
                else:
                    print('SKIPPED: ' + str(child))
                print(child.toecho())
                if len(child.children) != 0:
                    self.generate_report(child)

    def recurse_run_tests(self, node):
        label = node.label + 1
        for child in node.children:
            if child.label == label:
                child.run(self)
                if len(child.children) != 0:
                    self.recurse_run_tests(child)

    def run_tests(self):
        self.root = initiate_tests()
        self.root.run(self)
        self.recurse_label_tests(self.root)
        self.recurse_run_tests(self.root)

        print('SERVER: ' + self.base_url)
        print('VARIABLES: ' + str(self.session_params))
        print('TOTAL TEST CASES: ' + str(self.total_tests))
        print('TOTAL TEST CASES PASSED: ' + str(self.total_tests_passed))
        print('TOTAL TEST CASES SKIPPED: ' + str(self.total_tests_skipped))
        print('TOTAL TEST CASES FAILED: ' + str(self.total_tests_failed))

        self.generate_report(self.root)


tests = [
]

if __name__ == "__main__":
    tr = TestRunner('https://www.ebi.ac.uk/ena/cram/')
    tr.run_tests()

    print('--------------')

    tr = TestRunner('http://localhost:5000/')
    tr.run_tests()
