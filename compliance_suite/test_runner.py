from tests import initiate_tests


def recurse_label_tests(root):
    label = root.label + 1
    for child in root.children:
        if label > child.label:
            child.label = label
        if len(child.children) != 0:
            recurse_label_tests(child)


class TestRunner():
    def __init__(self, base_url):
        self.root = None
        self.session_params = {
            'info_implement': None,
            'metadata_implement': None,
            'limit': None,
            'trunc512': None,
            'circular': None,
            'redirection': None
        }

        self.test_results = []
        self.base_url = base_url

    def generate_report(self, node):
        label = node.label + 1
        for child in node.children:
            if child.label == label:
                print(child.algorithm.__name__ + ' ' + str(child.label) + ' ' + str(child.result))
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
        recurse_label_tests(self.root)
        self.recurse_run_tests(self.root)
        self.generate_report(self.root)


tests = [
    'info_implementation'
    'info_default_encoding',
    'info_content_type',
    'info_circular',
    'info_subsequence_limit',
    'info_alorithms',
    'info_api_version',

    'metadata_implementation',
    'metadata_default_encoding',
    'metadata_md5',
    'metadata_trunc512',
    'metadata_length',
    'metadata_aliases'
    'metadata_trunc512',
    'metadata_content_type',
    'metadata_invalid_checksum_404_error'
]

if __name__ == "__main__":
    tr = TestRunner('http://localhost:5000/')
    tr.run_tests()
