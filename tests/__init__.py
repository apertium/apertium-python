import os
import sys
import unittest

from streamparser import (
    parse, SReading, known, unknown,
)

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

import apertium # noqa: E402

class TestAnalyze(unittest.TestCase):
    
    def test_en(self):
        lexical_units = apertium.analyze('cats', 'en')
        lexical_unit = lexical_units[0]
        self.assertEqual(str(lexical_unit), 'cats/cat<n><pl>')
        readings = lexical_unit.readings
        self.assertListEqual(readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])

    def test_formatting(self):
        lexical_units = apertium.analyze('dogs', 'en', formatting='html')
        lexical_unit = lexical_units[0]
        self.assertEqual(str(lexical_unit), 'dogs/dog<n><pl>')
        readings = lexical_unit.readings
        self.assertListEqual(readings, [[SReading(baseform='dog', tags=['n', 'pl'])]])

    def test_error(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            apertium.analyze('cats', 'spa')

class TestGenerate(unittest.TestCase):

    def test_en(self):
        lexical_units = apertium.generate('cat<n><pl>', 'en')
        self.assertEqual(str(lexical_units), 'cats')

    def test_error(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            apertium.generate('cat<n><pl>', 'spa')

