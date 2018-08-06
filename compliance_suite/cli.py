import click
import os
import json
import tarfile

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
        print('yo')
        new_file_name = file_name + '_' + str(val)
        valid_file_name(new_file_name, val+1)
    return file_name


@click.group()
def main():
    pass


@main.command(help='run compliance utility report using base urls')
@click.option('--server', '-s', multiple=True, help='base_url')
@click.option(
    '--output_filename',
    '-fn', default='web', help='to create a tar.gz file')
@click.option(
    '--serve', is_flag=True, help='spin up a server')
def report(server, output_filename, serve):
    '''
    CLI command report to execute the report session and generate report on
    terminal, html file and json file if provided by the user

    Required arguments:
        server - Atleast one server is required. Multiple can be provided

    Optional arguments:
        --output_filename - file name for w:gz file of web folder. Default is web
    '''
    final_json = []
    if len(server) == 0:
        raise Exception('No server url provided. Provide atleast one')
    for s in server:
        tr = TestRunner(s)
        tr.run_tests()
        final_json.append(tr.generate_final_json())

    WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

    with open(os.path.join(WEB_DIR, 'temp_result' + '.json'), 'w+') as outfile:
        json.dump(final_json, outfile)

    index = 0
    while(os.path.exists(output_filename + '_' + str(index) + '.tar.gz')):
        index = index + 1
    with tarfile.open(output_filename + '_' + str(index) + '.tar.gz', "w:gz") as tar:
        tar.add(WEB_DIR, arcname=os.path.basename(WEB_DIR))

    if serve is True:
        start_mock_server()


if __name__ == "__main__":
    main()
