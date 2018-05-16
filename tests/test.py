import sys
import os
import unittest

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

from analysis.main import Analyzer

a = Analyzer('../langdata/apertium-eng/')


class TestUM(unittest.TestCase):

    def test_en(self):
        self.assertEqual(str(Analyzer.analyze(a, 'cats', 'en')), 'cats/cat<n><pl>')
        self.assertEqual(str(Analyzer.analyze(a, 'dogs', 'en')), 'dogs/dog<n><pl>')



if __name__ == '__main__':
    unittest.main()
