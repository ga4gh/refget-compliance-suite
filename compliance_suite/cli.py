import click
import os
import json
import tarfile
import sys

from compliance_suite.test_runner import TestRunner
from compliance_suite.report_server import start_mock_server
from ga4gh.testbed.report.report import Report
from ga4gh.testbed.submit.report_submitter import ReportSubmitter

def scan_for_errors(json):
    '''
    Routine used to loop through the available results data structure and generate
    high-level summaries for the four main test routines

    - service info
    - metadata
    - sequence
    - sequence range
    '''

    high_level_summary={}
    for high_level_name in ('test_info_implement', 'test_metadata_implement', 'test_sequence_implement', 'test_sequence_range'):
        # We are successful unless proven otherwise
        result=1
        for test in json[0]["test_results"]:
            if high_level_name in test["parents"]:
                if test['warning']:
                    result = test["result"]
                    break
        high_level_summary[high_level_name] =  {
            'result' : result,
            'name': high_level_name
        }
    json[0]["high_level_summary"] = high_level_summary


@click.group()
def main():
    pass


@main.command(help='run compliance utility report using base urls')
@click.option('--server', '-s', multiple=False, help='base_url')
@click.option(
    '--file_path_name',
    '-fpn', default='web', help='to create a tar.gz file')
@click.option(
    '--json_path',
    '--json', help='create a json file report. Setting this to "-" will emit to standard out')
@click.option(
    '--serve', is_flag=True, help='spin up a server')
@click.option(
    '--no-web', is_flag=True, help='skip the creation of a tarball')
@click.option(
    '--port', default=15800, help='port at which the compliance report is served')
@click.option(
    '--pretty', is_flag = True, help='JSON report pretty print')
@click.option(
    '--submit', is_flag = True, help='submit JSON report to testbed API')
@click.option(
    '--submit-id', help='report series ID')  
@click.option(
    '--submit-token', help='report series token') 
@click.option(
    '--submit-url', default="http://localhost:4500/reports", help='testbed API submission endpoint')
def report(server, file_path_name, json_path, serve, no_web, port, pretty, submit, submit_id, submit_token, submit_url):
    '''
    CLI command report to execute the report session and generate report on
    terminal, html file and json file if provided by the user

    Required arguments:
        server - At least one server is required. Multiple can be provided

    Optional arguments:
        --file_path_name - file name for w:gz file of web folder. Default is
        web_<int>.tar.gz
        --json_path - Provide a path to dump the final JSON content to
        --no-web - Avoid dumping a webfile
        --port - port at which the compliance report is served
    '''

    if len(server) == 0:
        raise Exception('No server url provided. Provide at least one')
    if submit:
        if submit_id == None: 
            raise Exception('Submit requested but no submit ID is provided')
        if submit_token == None:
            raise Exception('Submit requested but no submit token is provided')

    tr = TestRunner(server)
    tr.run_tests()
    ga4gh_report = tr.generate_report()
    final_json = ga4gh_report.to_json(pretty=pretty)
    

    if json_path is not None:
        if json_path == '-':
            json.dump(final_json, sys.stdout)
        else:
            with open(json_path, 'w') as outfile:
                #json.dump(final_json, outfile)
                outfile.write(final_json)

    WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

    if not no_web:
        if file_path_name is not None:
            with open(os.path.join(WEB_DIR, 'temp_result' + '.json'), 'w+') as outfile:
                outfile.write(final_json)

            index = 0
            while(os.path.exists(file_path_name + '_' + str(index) + '.tar.gz')):
                index = index + 1
            with tarfile.open(file_path_name + '_' + str(index) + '.tar.gz', "w:gz") as tar:
                tar.add(WEB_DIR, arcname=os.path.basename(WEB_DIR))

    if submit:
        print("Attempting to submit to testbed API...")
        response = ReportSubmitter.submit_report(submit_id, submit_token, ga4gh_report, url=submit_url)
        if response["status_code"] == 200:
            print("The submission was successful, the report ID is " + response["report_id"])
        else:
            print("The submission failed with a status code of " + str(response["status_code"]))
            print("Error Message: " + str(response["error_message"]))

    if serve is True:
        start_mock_server(port=port)


if __name__ == "__main__":
    main()