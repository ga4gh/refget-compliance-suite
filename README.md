# gsoc2018-ref-retrieval-api
Repository for the Google Summer of Code for the Reference Retrieval API

## Compliance Documentation
[Compliance Document](http://compliancedoc.readthedocs.io/en/latest/)

To generate this documentation locally, follow these steps:  
```bash
git clone https://github.com/ga4gh/gsoc2018-ref-retrieval-api.git

cd gsoc2018-ref-retrieval-api

pip3 install mkdocs  

mkdocs serve
```

## Compliance Test Suite
Compliance test suite is an API testing suite for reference server.

To run the tests, follow these steps:
```bash
git clone https://github.com/ga4gh/gsoc2018-ref-retrieval-api.git

cd gsoc2018-ref-retrieval-api/test_suite

pip3 install -r requirements.txt
```

If the server to be tested supports circular sequences then run

```
py.test --server <your-server-base-url-without-http://-prefix> --cir
```

and if it doesn't support circular sequences then run

```
py.test --server <your-server-base-url-without-http://-prefix>
```

If the server to be tested supports trunc512 algorithm then run

```
py.test --server <your-server-base-url-without-http://-prefix> --trunc512
```

and if it doesn't support trunc512 algorithm then run

```
py.test --server <your-server-base-url-without-http://-prefix>
```



If the server to be tested redirects success queries then run

```
py.test --server <your-server-base-url-without-http://-prefix> --redir
```

and if it doesn't redirects then run

```
py.test --server <your-server-base-url-without-http://-prefix>
```

You can try multiple combinations of these flags as per the server implementation for example

```bash
py.test --server <your-server-base-url-without-http://-prefix> --cir --trunc512

py.test --server <your-server-base-url-without-http://-prefix> --cir --redir

py.test --server <your-server-base-url-without-http://-prefix> --redir --trunc512

py.test --server <your-server-base-url-without-http://-prefix> --cir --trunc512 --redir

```
