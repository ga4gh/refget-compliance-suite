import click
try:
    from compliance_suite.test_runner import TestRunner
    from compliance_suite.report_utility import *
except:
    from test_runner import TestRunner
    from report_utility import *


@click.group()
def main():
    pass


@main.command(help='run compliance utility report using base urls')
@click.option('--server', '-s', multiple=True, help='base_url')
@click.option('--verbose', '-v', is_flag=True, help='to view the description and failure stack')
@click.option('--veryverbose', '-vv', is_flag=True, help='to view the description and failure stack')
@click.option('--html', '-ht', default=None, help='generate html file')
@click.option('--json', '-js', defult=None, help='generate json file')
def report(server, veryverbose, verbose, html, json):
    '''
    CLI command report to execute the report session and generate report on
    terminal, html file and json file if provided by the user

    Required arguments:
        server - Atleast one server is required. Multiple can be provided

    Optional arguments:
        --html - html file name for compliance matrix generation on html
        --json - json file name for machine readability

    Optional flags:
        -v - verbose for descriptive report on terminal
        --vv - veryverbose for even more description on terminal
        --of - only failure cases in the report on terminal
    '''
    final_json = []
    for s in server:
        tr = TestRunner(s)
        tr.run(verbose, veryverbose, only_failures)
        final_json.append(tr.generate_final_json())

    if html is not None:
        generate_html_file(final_json, html)

    if json is not None:
        generate_json_file(final_json, json)


if __name__ == "__main__":
    main()
