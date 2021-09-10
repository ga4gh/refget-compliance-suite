[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Travis (.org) branch](https://app.travis-ci.com/yash-puligundla/refget-compliance-suite.svg?branch=feature%2Fadd_unittesting)](https://app.travis-ci.com/yash-puligundla/refget-compliance-suite) [![Coverage Status](https://coveralls.io/repos/github/yash-puligundla/refget-compliance-suite/badge.svg?branch=feature/add_unittesting)](https://coveralls.io/github/yash-puligundla/refget-compliance-suite?branch=feature/add_unittesting) [![Read the Docs](https://img.shields.io/badge/docs-passing-brightgreen.svg)](http://samtools.github.io/hts-specs/refget.html) [![PyPI](https://img.shields.io/badge/pypi-v0.1.0-blue)](https://pypi.org/project/refget/) [![Python 3.6|3.7](https://img.shields.io/badge/python-3.6%20|%203.7-blue.svg?)](https://www.python.org)

# Refget Compliance Suite

Repository for the [refget API](http://samtools.github.io/hts-specs/refget.html) Compliance document and test suite.

## Important URLS

- [Refget specification](http://samtools.github.io/hts-specs/refget.html)
- [Compliance Document](https://compliancedoc.readthedocs.io/en/latest/)
- [Compliance utility documentation](https://compliancedoc.readthedocs.io/en/latest/utility/)

## Installing the compliance suite

```bash
pip3 install refget-compliance
```

## Running the compliance suite natively

The following will generate a HTML report for your server and serve said HTML. It will also generate a tarball locally of the report

```bash
refget-compliance report -s https://refget.server.com/ --serve
```

The following will generate a JSON report of your server:

```bash
refget-compliance report -s https://refget.server.com/ --json server.json
```

Setting `--json -` will have the compliance suite write the JSON to STDOUT.

## Running the compliance suite via docker

### Pull the docker image from dockerhub

```bash
docker pull ga4gh/refget-compliance-suite:{version}
```
{version} specifies the version of the docker image being pulled

### Spinning up a docker container

```bash
docker run -d -p 15800:15800 --name refget-compliance-suite ga4gh/refget-compliance-suite --server https://www.ebi.ac.uk/ena/cram/ --port 15800 --serve
```
#### Arguments:
- `--server` or `-s` (required). It is the url of the refget server being tested. At least one `--server` argument is required. Multiple can be provided.
- `--serve` (optional) It's default value is False. If `--serve` flag is True then the complaince report will be served on the specified port.
- `--port` (optional) It's default value is 15800. If `--port` is specified then this port has to be mapped and published on the docker container by changing the -p option of the docker run command. For example, if `--port 8080` is specified, then docker run command will be
```bash
docker run -d -p 8080:8080 --name refget-compliance-suite ga4gh/refget-compliance-suite --server https://www.ebi.ac.uk/ena/cram/ --port 8080 --serve
```
- `--json` or `--json_path` (optional) If this argument is '-' then the output json is flushed to standard output. If a valid path is provided then the output is written as a json file at the specified location.
- `--file_path_name` or `-fpn` (optional) It's default value is "web". This argument is required to create a ".tar.gz" format of the output json with the specified name.
- `--no-web` (optional) If `--no-web` flag is True then the ".tar.gz" output file creation will be skipped.

# Additional components

## Building and uploading the package to PyPI

First complete the following

1. Edit the files and test these changes are working
2. Update `setup.py` and increment the version number. Remember to use semantic versioning
3. Update CHANGELOG with all the changes you've made
4. Commit the above changes
5. Tag the repo with your version number e.g. `git tag -a 'release/1.2.6' -m 'Release v 1.2.6'`

Then run the following and provide your user credentials before doing this. This will upload the compliance suite to the test PyPI server.

```bash
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Assuming this works then upload to live PyPI and provide your live login details.

```bash
twine upload dist/*
```

If `twine` cannot be found on your machine run `pip3 install twine` or check in `$HOME/.local/bin` for the binary (sometimes python binaries end up in the `.local` directory).

## Compliance Documentation

To generate this documentation locally, follow these steps:

```bash
git clone https://github.com/ga4gh/refget-compliance.git

cd refget-compliance

pip3 install mkdocs

mkdocs serve
```

## Unittests

To run the tests, follow these steps:

### Clone the repository and install required packages
```bash
git clone https://github.com/ga4gh/refget-compliance.git

cd refget-compliance-suite

pip3 install -r unittests/requirements.txt
```

### Deploy the good and bad mock servers:
The good mock server is an ideal implementation of refget standard. It runs on port 8989. The bad mock server does not adhere to refget standards and it runs on port 8988. The port numbers can be configured by changing the GOOD_SERVER_URL and BAD_SERVER_URL values in unittests/constants.py file.
```bash
python3 unittests/good_mock_server.py &
python3 unittests/bad_mock_server.py &
```

### Run the unittests

```bash
py.test 
```