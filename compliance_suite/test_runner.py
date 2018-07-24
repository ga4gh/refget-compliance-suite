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
        self.results = []

    def recurse_label_tests(self, root):
        label = root.label + 1
        for child in root.children:
            if label > child.label:
                self.total_tests = self.total_tests + 1
                child.label = label
            if len(child.children) != 0:
                self.recurse_label_tests(child)

    def recurse_generate_json(self, node):
        label = node.label + 1
        for child in node.children:
            if child.label == label:
                test_result_object = {
                    'name': str(child),
                    'result': child.result,
                    # 'test_description': child.description,
                    'text': child.toecho(),
                    'parents': child.parents,
                    'children': child.children
                }
                if child.result == 1:
                    self.total_tests_passed = self.total_tests_passed + 1
                elif child.result == -1:
                    self.total_tests_failed = self.total_tests_failed + 1
                else:
                    self.total_tests_skipped = self.total_tests_skipped + 1
                self.results.append(test_result_object)
                if len(child.children) != 0:
                    self.recurse_generate_json(child)

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
        self.recurse_generate_json(self.root)


if __name__ == "__main__":
    tr = TestRunner('https://www.ebi.ac.uk/ena/cram/')
    tr.run_tests()

    print('--------------')

    # tr = TestRunner('http://localhost:5000/')
    # tr.run_tests()
