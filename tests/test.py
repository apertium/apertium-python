import sys
import os
import unittest

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../Apertium/analysis')
sys.path.append(base_path)

from main import Analyzer  # noqa: E402

a = Analyzer()


class TestAnalyze(unittest.TestCase):

    def test_en(self):
        self.assertEqual(str(Analyzer.analyze(a, 'cats', 'en')), 'cats/cat<n><pl>')


if __name__ == '__main__':
    unittest.main()
