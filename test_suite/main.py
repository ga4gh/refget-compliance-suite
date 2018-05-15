import argparse
import unittest
from sequence_api_tests import SequenceAPITests


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Test Suite for Reference Servers")
    parser.add_argument(
        'base_url',
        help='Server base url'
        )
    parser.add_argument(
        '--cir',
        dest='circular_support',
        action='store_const',
        const=True,
        default=False,
        help='Does the server supports circular chromosomes (defaults to "NO")'
        )
    return parser.parse_args()


def main():
    arguments = get_arguments()
    try:
        base_url = 'http://' + str(arguments.base_url) + '/'
    except IOError:
        print("Enter server's base url")
    circular_support = arguments.circular_support

    SequenceAPITests.base_url = base_url + 'sequence/'
    SequenceAPITests.is_circular_support = circular_support

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(SequenceAPITests()))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)


if __name__ == "__main__":
    main()
