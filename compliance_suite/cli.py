import click
import os
import json
import tarfile
import sys

from compliance_suite.test_runner import TestRunner
from compliance_suite.report_server import start_mock_server

# try:
#     from compliance_suite.test_runner import TestRunner
#     from compliance_suite.report_server import start_mock_server
# except:
#     from test_runner import TestRunner
#     from report_server import start_mock_server


def valid_file_name(file_name, val):
    if os.path.exists(file_name):
        print('yo', file=sys.stderr)
        new_file_name = file_name + '_' + str(val)
        valid_file_name(new_file_name, val+1)
    return file_name

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
@click.option('--server', '-s', multiple=True, help='base_url')
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
def report(server, file_path_name, json_path, serve, no_web):
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
    '''
    final_json = []
    if len(server) == 0:
        raise Exception('No server url provided. Provide at least one')
    for s in server:
        tr = TestRunner(s)
        tr.run_tests()
        final_json.append(tr.generate_final_json())

    scan_for_errors(final_json)

    if json_path is not None:
        if json_path == '-':
            json.dump(final_json, sys.stdout)
        else:
            with open(json_path, 'w') as outfile:
                json.dump(final_json, outfile)

    WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

    if not no_web:
        if file_path_name is not None:
            with open(os.path.join(WEB_DIR, 'temp_result' + '.json'), 'w+') as outfile:
                json.dump(final_json, outfile)

            index = 0
            while(os.path.exists(file_path_name + '_' + str(index) + '.tar.gz')):
                index = index + 1
            with tarfile.open(file_path_name + '_' + str(index) + '.tar.gz', "w:gz") as tar:
                tar.add(WEB_DIR, arcname=os.path.basename(WEB_DIR))

    if serve is True:
        start_mock_server()


if __name__ == "__main__":
    main()
