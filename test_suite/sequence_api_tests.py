import unittest
from urllib.request import urlopen


class SequenceAPITests(unittest.TestCase):
    base_url = ''
    is_circular_support = False

    def setUp(self):
        pass

    def test_non_ranged_circular_chromosome_default_encoding(self):
        I_trunc512 = '2085c82d80500a91dd0b8aa9237b0e43f1c07809bd6e6785'
        testurl = self.base_url + I_trunc512
        response = urlopen(testurl)
        content = response.read().decode("utf-8")
        self.assertEqual('GAGTTTTATC', content[:10])
        self.assertEqual(response.code, 200)

    def tearDown(self):
        pass
