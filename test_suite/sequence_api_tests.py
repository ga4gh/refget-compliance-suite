import unittest
import requests
import sys
import os

from chromosome_model import db, Chromosome
from utils import populate_db


def get(testurl, headers=None, die_on_errors=True):
        response = requests.get(testurl, headers={"Accept": "text/plain"})

        if (not response.ok) and die_on_errors:
            response.raise_for_status()
            sys.exit(-1)

        return response


class SequenceAPITests(unittest.TestCase):
    base_url = ''
    is_circular_support = False

    def setUp(self):
        db.connect()
        db.create_tables([Chromosome])
        populate_db()

    def test_non_ranged_chromosomes_default_encoding(self):
        self.assertEqual(
            Chromosome.get(Chromosome.name == 'NC').sequence,
            get(
                self.base_url + Chromosome.get(
                    Chromosome.name == 'NC').trunc512).text
            )
        self.assertEqual(
            Chromosome.get(Chromosome.name == 'I').sequence,
            get(
                self.base_url + Chromosome.get(
                    Chromosome.name == 'I').trunc512).text
            )
        self.assertEqual(
            Chromosome.get(Chromosome.name == 'VI').sequence,
            get(
                self.base_url + Chromosome.get(
                    Chromosome.name == 'VI').trunc512).text
            )

    def tearDown(self):
        os.remove('test_db.db')
