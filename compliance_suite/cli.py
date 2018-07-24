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
@click.option('--verbose', '-v', is_flag=True, help='to view the description and failure stack')
@click.option('--html', '-h', is_flag=True, help='generate html file')
@click.option('--json', '-j', is_flag=True, help='generate json file')
def sequence(server, verbose, html, json):
    '''maps to class method Fetcher.sequence for sequence retrieval
    '''
    for s in server:
        tr = TestRunner(s)
        tr.run(verbose, html, json)
    print(verbose)
    print(html)
    print(json)


if __name__ == "__main__":
    main()
