import sys
import os
import unittest

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

try:
    from analysis.main import Analyzer
except Exception:
    print('Error in import')
    raise

a = Analyzer('../langdata/apertium-eng/')


class TestUM(unittest.TestCase):

    def test_en(self):
        self.assertEqual(str(Analyzer.analyze(a, 'cats', 'en')), 'cats/cat<n><pl>')
        self.assertEqual(str(Analyzer.analyze(a, 'dogs', 'en')), 'dogs/dog<n><pl>')
        self.assertEqual(str(Analyzer.analyze(a, 'women', 'en')), 'women/woman<n><pl>')
        self.assertEqual(str(Analyzer.analyze(a, 'men', 'en')), 'men/man<n><pl>')
        self.assertEqual(str(Analyzer.analyze(a, 'books', 'en')), 'books/book<n><pl>/book<vblex><pres><p3><sg>')
        self.assertEqual(str(Analyzer.analyze(a, 'luggages', 'en')), 'luggages/luggage<n><pl>')


if __name__ == '__main__':
    unittest.main()
