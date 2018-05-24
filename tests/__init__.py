import os
import sys
import unittest

from streamparser import (
    parse, parse_file, SReading, known, unknown,
)

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

import apertium # noqa: E402

class TestAnalyze(unittest.TestCase):
    s = '$^%s$' % (apertium.analyze('cats', 'en')[0])

    def test_en(self):
        lexical_units = list(parse(self.s))
        self.assertEqual(len(lexical_units), 1)
        lexical_unit = lexical_units[0]
        print("this is the type", type(lexical_unit))
        self.assertEqual(str(lexical_unit), 'cats/cat<n><pl>')
        readings = lexical_unit.readings
        self.assertListEqual(readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

class TestGenerate(unittest.TestCase):
    s = '$^%s$' % (apertium.generate('cat<n><pl>', 'en'))

    def test_en(self):
        lexical_units = list(parse(self.s))
        self.assertEqual(len(lexical_units), 1)
        lexical_unit = lexical_units[0]
        self.assertEqual(str(lexical_unit), 'cats')
        self.assertEqual(lexical_unit.knownness, known)