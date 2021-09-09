import os
import glob
import json
from unittests.constants import *

TEST_SUITE = os.path.dirname(__file__)
SEQUENCE_FILES = os.path.join(TEST_SUITE, 'data/sequences/')

class Sequence:
    '''
    Sequence model object used to store sequence data in a defined manner
    '''
    def __init__(self, name, sequence, is_circular, sha512, md5, size):
        self.name = name
        self.sequence = sequence
        self.is_circular = is_circular
        self.sha512 = sha512
        self.md5 = md5
        self.size = size

# Additional utility functions to load the sequence data
def read_sequence(chr_name):
    with open(SEQUENCE_FILES + chr_name + ".faa", "r") as sequence_file:
        next(sequence_file)
        sequence_data = sequence_file.read().replace('\n', '')
    return sequence_data

def read_sequence_data(chr_name):
    with open(SEQUENCE_FILES + "checksums.json", "r") as checksums_file:
        checksums = json.load(checksums_file)
    return checksums[chr_name]

def get_seq_obj(chr):
    data = read_sequence_data(chr)
    if data['is_circular'] == 1:
        data['is_circular'] = True
    else:
        data['is_circular'] = False
    return Sequence(
        chr,
        read_sequence(chr),
        data['is_circular'],
        data['sha512'],
        data['md5'],
        len(read_sequence(chr))
    )

def set_data():
    '''
    data fixture loads all the data and return data variable for use in tests
    '''
    data = []
    data.append(get_seq_obj("I"))
    data.append(get_seq_obj("VI"))
    data.append(get_seq_obj("NC"))
    return data

def remove_output_dirs():
    '''
    remove output files created while unittesting
    '''
    file_names = []
    for name in glob.glob('./*'):
        file_names.append(name)
    for this_file in file_names:
        if this_file.endswith((".json",".tar.gz")) and this_file.startswith(('./'+JSON_REPORT,'./'+WEB_FILE_PATH,'./'+DEFAULT_WEB_DIR)):
            os.remove(this_file)

def get_sequence_obj(seq_id,DATA, TRUNC512):
    '''
    get_sequence_obj is used to get the sequence object from DATA
    based on the checksum identifier passed in the URL.
    '''
    for this_seq_obj in DATA:
        if this_seq_obj.md5 == seq_id:
            return this_seq_obj
        if TRUNC512 is True and this_seq_obj.sha512 == seq_id:
            return this_seq_obj
    return None