import unittests
from compliance_suite.test_runner import TestRunner

good_runner_v1 = TestRunner(unittests.constants.GOOD_SERVER_V1_URL)
good_runner_v1.session_params = {
    "refget_version": "1.0.0",
    "limit": 400000,
    "algorithms:trunc512": True,
    "circular_supported": True,
    "redirection": None
}
bad_runner_v1 = TestRunner(unittests.constants.BAD_SERVER_V1_URL)
bad_runner_v1.session_params = {
    "refget_version": "1.0.0",
    "limit": 400000,
    "algorithms:trunc512": True,
    "circular_supported": True,
    "redirection": None
}
good_runner_v2 = TestRunner(unittests.constants.GOOD_SERVER_V2_URL)
good_runner_v2.session_params = {
    "refget_version": "2.0.0",
    "limit": 400000,
    "algorithms:trunc512": False,
    "algorithms:ga4gh": True,
    "identifier_types:insdc": True,
    "circular_supported": True,
    "redirection": None
}
bad_runner_v2 = TestRunner(unittests.constants.BAD_SERVER_V2_URL)
bad_runner_v2.session_params = {
    "refget_version": "2.0.0",
    "limit": 400000,
    "algorithms:trunc512": False,
    "algorithms:ga4gh": True,
    "identifier_types:insdc": True,
    "circular_supported": True,
    "redirection": None
}
