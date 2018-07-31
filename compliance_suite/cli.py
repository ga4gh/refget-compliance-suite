import click
try:
    from compliance_suite.test_runner import TestRunner
except:
    from test_runner import TestRunner


@click.group()
def main():
    pass


@main.command(help='run compliance utility report using base urls')
@click.option('--server', '-s', multiple=True, help='base_url')
@click.option('--verbose', '-v', is_flag=True, help='to view the failure stack')
@click.option('--veryverbose', '-vv', is_flag=True, help='to view edge cases along with failure stack')
@click.option('--html', '-ht', default='html', help='generate html file')
@click.option('--json', '-js', deafult='json', help='generate json file')
def report(server, veryverbose, verbose, html, json):
    if verbose is True and veryverbose is True:
        raise Exception('Only one of -v and -vv can be used')
    if len(server) == 0:
        raise Exception('No server url provided. Provide atleast one')
    for s in server:
        tr = TestRunner(s)
        tr.run(verbose, html, json)
    print(verbose)
    print(html)
    print(json)


if __name__ == "__main__":
    main()
