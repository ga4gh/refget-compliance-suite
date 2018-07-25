import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
install_requires = ['requests', 'click']


setuptools.setup(
    name="compliance-suite-utility",
    version="0.0.1",
    author="Somesh Chaturvedi",
    author_email="somesh.08.96@gmail.com",
    description="A compliance utility reporting system for reference servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ga4gh/gsoc2018-ref-retrieval-api",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        compliance_utility=compliance_suite.cli:main
    ''',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
