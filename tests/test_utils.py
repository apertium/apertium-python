import unittest

from apertium import utils


class TestUtils(unittest.TestCase):
    """Unittests for apertium/utils.py"""

    def test_deformatter(self):
        """
        Test for utils.deformatter function
        Iunput: Test formatter
        Expected output: Test fromatter[][\n]
        """
        result = utils.deformatter('Test formatter')
        self.assertEqual('Test formatter[][\n]', result)

    def test_to_alpha3_code(self):
        """
        Test for utils.to_alpha3_code.
        Input: 'en_US'
        Expected output: 'eng_US'
        """
        result = utils.to_alpha3_code('en_US')
        self.assertEqual('eng_US', result)
