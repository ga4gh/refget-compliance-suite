Compliance Utility Report tool generates a detailed compliance report on the server using interdependent test cases on command line interface. It can also generate a comppliance matrix on a html page and a json file for machine readablity and extensibly.

# Getting Started

## Installation
Installation is a simple three step process.

```base
git clone https://github.com/ga4gh/refget-compliance-suite.git
cd refget-compliance-suite
python setup.py sdist bdist_wininst upload
```

## First test report

```base
compliance_utility report -s http://localhost:5000/
```
Note : prefixing with '**http://**' or '**https://**' (as per the server) and trailing slash '**/**' is important

Multiple servers can be tested at once by providing multiple `--server` or `-s` arguments

```base
compliance_utility report -s http://localhost:5000/ -s http://localhost:6000 - http://localhost:7000
```

## Arguments

### -s | --server
Required argument specifying server to be tested and for report to be generated. Can be multiple but must be atleast one.

### -fpn | --file_path_name
Optional argument to specify the path of tar.gz file to be stored. Path should be of the format `path/to/file/file_name.tar.gz`.  
By default it'll get stored by the name web_<some_integer>.tar.gz eg web_0.tar.gz, web_1.tar.gz etc.

### --serve
Optional flag to spin up a local server showing reports on web browser

## Sample Reports

### Text Report
![Alt text](assets/text.png?raw=true "Text Report")

### Compliance Matrix
![Alt text](assets/matrix.png?raw=true "Text Report")

### JSON Report
![Alt text](assets/json.png?raw=true "Text Report")
