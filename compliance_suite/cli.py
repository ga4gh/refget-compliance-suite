import click
try:
    from compliance_suite.test_runner import TestRunner
except:
    from test_runner import TestRunner


@click.group()
def main():
    pass


@main.command(help='run compliance utility report using base urls')
@click.option('--server', '-s', default=None, multiple=True, help='base_url')
def sequence(server):
    '''maps to class method Fetcher.sequence for sequence retrieval
    '''
    for s in server:
        test_runner = TestRunner(s)
        test_runner.run_tests()
        click.echo(test_runner.result)


if __name__ == "__main__":
    main()
