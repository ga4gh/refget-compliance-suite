Compliance Utility Report tool generates a detailed compliance report on the server using interdependent test cases on command line interface. It can also generate a comppliance matrix on a html page and a json file for machine readablity and extensibly.

# Installation
Installation is a simple three step process.

```base
git clone https://github.com/ga4gh/gsoc2018-ref-retrieval-api.git
cd gsoc2018-ref-retrieval-api
python setup.py sdist bdist_wininst upload
```

# Usage
Multiple servers can be tested at once by providing multiple `--server` or `-s` arguments

<h2> Example </h2>

```base
compliance_utility report --help
```


<h3> Optional Arguments </h3>

<h3> verbose -v</h3>

<h3> very verbose -vv </h3>

<h3> html -ht </h3>

<h3> json -js </h3>

<h3> only failures -of </h3>
