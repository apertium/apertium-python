import os
import sys
import unittest

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

# TODO: put this into __init__.py so that there's no need for main
from apertium.analysis.main import Analyzer  # noqa: E402

a = Analyzer()


class TestAnalyze(unittest.TestCase):
    def test_en(self):
        # TODO: test the LexicalUnit object instead! (see streamparser tests)
        self.assertEqual(str(Analyzer.analyze(a, 'cats', 'en')), 'cats/cat<n><pl>')


if __name__ == '__main__':
    unittest.main(buffer=True, verbosity=2)
