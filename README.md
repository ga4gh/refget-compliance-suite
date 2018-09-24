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

## Running the compliance suite

The following will generate a HTML report for your server and serve said HTML. It will also generate a tarball locally of the report

```bash
refget-compliance report -s https://refget.server.com/ --serve
```

The following will generate a JSON report of your server:

```bash
refget-compliance report -s https://refget.server.com/ --json server.json
```

Setting `--json -` will have the compliance suite write the JSON to STDOUT.

# Additional components

## Building and uploading the package to PyPI

First do your edits, test and update `setup.py` with your new version number. Then run the following and provide your user credentials before doing this. This will upload the compliance suite to the test PyPI server.

```bash
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Assuming this works then upload to live PyPI and provide your live login details.

```bash
twine upload dist/*
```

## Compliance Documentation

To generate this documentation locally, follow these steps:

```bash
git clone https://github.com/ga4gh/refget-compliance.git

cd refget-compliance

pip3 install mkdocs

mkdocs serve
```

## Compliance Test Suite

Compliance test suite is an API testing suite for refget servers.

To run the tests, follow these steps:

```bash
git clone https://github.com/ga4gh/refget-compliance.git

cd refget-compliance-suite/test_suite

pip3 install -r requirements.txt
```

If the server to be tested supports circular sequences then run

```bash
py.test --server <your-server-base-url-without-http://-prefix> --cir
```

and if it doesn't support circular sequences then run

```bash
py.test --server <your-server-base-url-without-http://-prefix>
```

If the server to be tested supports trunc512 algorithm then run

```bash
py.test --server <your-server-base-url-without-http://-prefix> --trunc512
```

and if it doesn't support trunc512 algorithm then run

```bash
py.test --server <your-server-base-url-without-http://-prefix>
```

If the server to be tested redirects success queries then run

```bash
py.test --server <your-server-base-url-without-http://-prefix> --redir
```

And if it doesn't redirects then run

```bash
py.test --server <your-server-base-url-without-http://-prefix>
```

You can try multiple combinations of these flags as per the server implementation for example

```bash
py.test --server <your-server-base-url-without-http://-prefix> --cir --trunc512

py.test --server <your-server-base-url-without-http://-prefix> --cir --redir

py.test --server <your-server-base-url-without-http://-prefix> --redir --trunc512

py.test --server <your-server-base-url-without-http://-prefix> --cir --trunc512 --redir
```
