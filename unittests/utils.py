import os
import glob
import json

import compliance_suite
from unittests.constants import *

SEQUENCE_FILES = os.path.join(os.path.dirname(compliance_suite.__file__), 'sequences')


class Sequence:
    """
    Sequence model object used to store sequence data in a defined manner
    """
    def __init__(self, name, sequence, is_circular, sha512, md5, ga4gh, insdc, size):
        self.name = name
        self.sequence = sequence
        self.is_circular = is_circular
        self.sha512 = sha512
        self.md5 = md5
        self.ga4gh = ga4gh
        self.insdc = insdc
        self.size = size


# Additional utility functions to load the sequence data
def read_sequence(chr_name):
    with open(os.path.join(SEQUENCE_FILES, chr_name + ".faa"), "r") as sequence_file:
        next(sequence_file)
        sequence_data = sequence_file.read().replace('\n', '')
    return sequence_data


def read_sequence_data(chr_name):
    with open(os.path.join(SEQUENCE_FILES, "checksums.json"), "r") as checksums_file:
        checksums = json.load(checksums_file)
    return checksums[chr_name]


def get_seq_obj(chr):
    data = read_sequence_data(chr)
    sequence = read_sequence(chr)
    if data['is_circular'] == 1:
        data['is_circular'] = True
    else:
        data['is_circular'] = False
    return Sequence(
        name=chr, sequence=sequence, is_circular=data['is_circular'], sha512=data['sha512'],
        md5=data['md5'], ga4gh=data['ga4gh'], insdc=data['insdc'], size=len(sequence)
    )


def set_data():
    """
    data fixture loads all the data and return data variable for use in tests
    """
    return [
        get_seq_obj("I"),
        get_seq_obj("VI"),
        get_seq_obj("NC")
    ]


def remove_output_dirs():
    """
    remove output files created while unittesting
    """
    file_names = []
    current_working_dir = os.path.dirname(__file__)
    root_dir = current_working_dir.split("refget-compliance-suite")[0]+"refget-compliance-suite/"
    for name in glob.glob(root_dir+'*'):
        file_names.append(name)
    for this_file in file_names:
        if this_file.endswith((".json",".tar.gz")) and \
                this_file.startswith((root_dir+JSON_REPORT, root_dir+WEB_FILE_PATH, root_dir+DEFAULT_WEB_DIR)):
            os.remove(this_file)


def get_sequence_obj(seq_id, DATA, TRUNC512, GA4GH, INSDC):
    '''
    get_sequence_obj is used to get the sequence object from DATA
    based on the checksum identifier passed in the URL.
    '''
    for this_seq_obj in DATA:
        if this_seq_obj.md5 == seq_id:
            return this_seq_obj
        if TRUNC512 is True and this_seq_obj.sha512 == seq_id:
            return this_seq_obj
        if GA4GH is True and this_seq_obj.ga4gh == seq_id:
            return this_seq_obj
        if INSDC is True and this_seq_obj.insdc == seq_id:
            return this_seq_obj
