import argparse


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
        base_url = arguments.base_url
    except IOError:
        print("Enter server's base url")
    circular_support = arguments.circular_support
    # test(base_url, circular_support)


if __name__ == "__main__":
    main()
