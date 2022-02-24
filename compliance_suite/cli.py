import click
import os
import json
import tarfile
import sys
import ga4gh

from compliance_suite.test_runner import TestRunner
from compliance_suite.report_server import start_mock_server
from ga4gh.testbed.report.report import Report

def scan_for_errors(json):
    '''
    Routine used to loop through the available results data structure and generate
    high-level summaries for the four main test routines

    - service info
    - metadata
    - sequence
    - sequence range
    '''
    # print('#### inside scan_for_errors ####')
    # print('json: {}'.format(json))
    #print(json)
    high_level_summary={}
    for high_level_name in ('test_info_implement', 'test_metadata_implement', 'test_sequence_implement', 'test_sequence_range'):
        # We are successful unless proven otherwise
        result=1
        for test in json["test_results"]:
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
@click.option(
    '--port', default=15800, help='port at which the compliance report is served')
def report(server, file_path_name, json_path, serve, no_web, port):
    '''
    CLI command report to execute the report session and generate report on
    terminal, html file and json file if provided by the user

    Required arguments:
        server - At least one server is required. Multiple can be providedpython

    Optional arguments:
        --file_path_name - file name for w:gz file of web folder. Default is
        web_<int>.tar.gz
        --json_path - Provide a path to dump the final JSON content to
        --no-web - Avoid dumping a webfile
        --port - port at which the compliance report is served
    '''

    #final_json = []
    if len(server) == 0:
        raise Exception('No server url provided. Provide at least one')
    for s in server:
        tr = TestRunner(s)
        tr.run_tests()
        #final_json.append(tr.generate_final_json())
        #final_json.append(tr.generate_report().to_json())
    
    final_json = tr.generate_report().to_json()

    if json_path is not None:
        if json_path == '-':
            json.dump(final_json, sys.stdout)
        else:
            with open(json_path, 'w') as outfile:
                #json.dump(final_json, outfile)
                outfile.write(str(final_json))

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
        start_mock_server(port=port)


if __name__ == "__main__":
    main()