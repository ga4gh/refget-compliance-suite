import pytest

# decorator for tests to be skipped if redirection is implemented in the server
redirection_false_skip = pytest.mark.skipif(
    "pytest.config.getoption('--redir') == 'False'")

# decorator for tests to be skipped if redirection is not implemented in the
# server
redirection_true_skip = pytest.mark.skipif(
    "pytest.config.getoption('--redir') != 'False'")

# decorator for tests to be skipped if circular chromosome is not
# supported by the server
circular_support_false_skip = pytest.mark.skipif(
    ("pytest.config.getoption('--cir') == 'False'"))

# decorator for tests to be skipped if circular chromosome is supported by the
# server
circular_support_true_skip = pytest.mark.skipif(
    "pytest.config.getoption('--cir') != 'False'")


# decorator for tests to be skipped if trunc512 is not
# supported by the server
trunc512_support_false_skip = pytest.mark.skipif(
    ("pytest.config.getoption('--trunc512') == 'False'"))

# decorator for tests to be skipped if trunc512 is supported by the
# server
trunc512_support_true_skip = pytest.mark.skipif(
    "pytest.config.getoption('--trunc512') != 'False'")
