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
        self.assertListEqual(lexical_unit.readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            apertium.analyze('cats', 'spa')

class TestGenerate(unittest.TestCase):
    def test_en(self):
        wordform = apertium.generate('cat<n><pl>', 'en')
        self.assertEqual(wordform, 'cats')

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            apertium.generate('cat<n><pl>', 'spa')
