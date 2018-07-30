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
