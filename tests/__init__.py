import os
import sys
import unittest

from streamparser import parse, SReading, known

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

import apertium  # noqa: E402


class TestAnalyze(unittest.TestCase):

    def test_en(self):
        analyzer = apertium.Analyzer('en')
        lexical_units = analyzer.analyze('cats')
        lexical_unit = lexical_units[0]
        self.assertListEqual(lexical_unit.readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            analyzer = apertium.Analyzer('spa')


class TestGenerate(unittest.TestCase):

    def test_single(self):
        generator = apertium.Generator('en')
        wordform = generator.generate('^cat<n><pl>$')
        self.assertEqual(wordform, 'cats')

    def test_multiple(self):
        generator = apertium.Generator('en')
        lexical_units = generator.generate('^cat<n><pl>$ ^cat<n><pl>$')
        self.assertEqual(lexical_units, 'cats cats')

    def test_bare(self):
        generator = apertium.Generator('en')        
        lexical_units = generator.generate('cat<n><pl>')
        self.assertEqual(lexical_units, 'cat<n><pl>')

    def test_uninstalled_mode(self):
        generator = apertium.Generator('spa')
        with self.assertRaises(apertium.ModeNotInstalled):
            generator.generate('cat<n><pl>')


class TestTranslate(unittest.TestCase):

    def test_en_spa(self):
        translator = apertium.Translator('eng', 'spa')
        translated = translator.translate('cats')
        self.assertEqual(translated, 'Gatos')
