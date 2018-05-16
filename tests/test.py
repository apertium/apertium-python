import os
import sys
import unittest

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

import analysis
import analysis.modesearch
from analysis.main import Analyzer


a = Analyzer('../langdata/apertium-eng/')
 
class TestUM(unittest.TestCase):

    def test_en(self):
        self.assertEqual(str(Analyzer.analyze(a, 'cats', 'en')), "cats/cat<n><pl>")

 
if __name__ == '__main__':
    unittest.main()