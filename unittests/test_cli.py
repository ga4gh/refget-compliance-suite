"""Module unittests.test_cli.py
This module contains methods to test the cli module via pytest.
"""
import pytest
import json
import mock
import click
from click.testing import CliRunner
from unittests.utils import remove_output_dirs
from compliance_suite.cli import *
from unittests.constants import GOOD_SERVER_URL as good_mock_server, JSON_REPORT, WEB_FILE_PATH

# TO DO patch start_mock_server and provide the --serve option. Assert that start_mock_server is called once & with port
# TO DO add cases with exit code 1


def test_invoke_main():
    """
    asserts that the 'main' method of cli module can be executed
    """

    runner = CliRunner()
    runner.invoke(main)
    assert True


def test_scan_for_errors():
    """
    asserts that high_level_summary is correct -
    0. when there are no warnings in final_json
    1. when there are warnings in final_json
    """

    final_json = json.loads(
        open("unittests/data/json_reports/final_json_0.json", "r").read()
    )
    expected_high_level_summary = json.loads(
        open("unittests/data/json_reports/high_level_summary_0.json", "r").read()
    )
    scan_for_errors(final_json)
    actual_high_level_summary = final_json[0]["high_level_summary"]
    assert json.dumps(expected_high_level_summary, sort_keys=True)== json.dumps(actual_high_level_summary, sort_keys=True)


    final_json = json.loads(
        open("unittests/data/json_reports/final_json_1.json", "r").read()
    )
    expected_high_level_summary = json.loads(
        open("unittests/data/json_reports/high_level_summary_1.json", "r").read()
    )
    scan_for_errors(final_json)
    actual_high_level_summary = final_json[0]["high_level_summary"]
    assert json.dumps(expected_high_level_summary, sort_keys=True)== json.dumps(actual_high_level_summary, sort_keys=True)

def test_report():
    '''
    test report() with different combinations of input args 
    '''
    # required argument "--server" is missing
    remove_output_dirs()
    runner = CliRunner()
    result = runner.invoke(report, [])
    assert result.exit_code == 1
    remove_output_dirs()
    
    # with --server
    runner = CliRunner()
    result = runner.invoke(report, ["--server", good_mock_server])
    assert result.exit_code == 0
    remove_output_dirs()

    # with --server and --port
    runner = CliRunner()
    result = runner.invoke(report, ["--server", good_mock_server, "--port", "15900"])
    assert result.exit_code == 0
    remove_output_dirs()

    ## TODO: mock start_mock_server
    # runner = CliRunner()
    # result = runner.invoke(report, ["--server", good_mock_server, "--serve"])
    # assert result.exit_code == 0
    # remove_output_dirs()

    # with a bad "--port" arg
    runner = CliRunner()
    result = runner.invoke(report, ["--server", good_mock_server, "--json",JSON_REPORT,"--port","abcd"])
    assert result.exit_code == 2
    remove_output_dirs()


    runner = CliRunner()
    result = runner.invoke(report, ["--server", good_mock_server,"--file_path_name",WEB_FILE_PATH,"--json",JSON_REPORT])
    assert result.exit_code == 0
    remove_output_dirs()

    # with a bad "--server" args
    runner = CliRunner()
    result = runner.invoke(report, ["--server", "http://dfgh.ghj/","--file_path_name",WEB_FILE_PATH,"--json",JSON_REPORT])
    assert result.exit_code == 1
    remove_output_dirs()    