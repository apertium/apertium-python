import os
import sys
import unittest

from streamparser import parse, SReading, known

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

import apertium  # noqa: E402


class TestAnalyze(unittest.TestCase):
    def test_analyzer_en(self):
        analyzer = apertium.Analyzer('en')
        lexical_units = analyzer.analyze('cats')
        lexical_unit = lexical_units[0]
        self.assertListEqual(lexical_unit.readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

    def test_analyze_en(self):
        lexical_units = apertium.analyze('eng', 'cats')
        lexical_unit = lexical_units[0]
        self.assertListEqual(lexical_unit.readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            analyzer = apertium.Analyzer('spa')

    def test_repr(self):
        analyzer = apertium.Analyzer('en')
        self.assertEqual(repr(analyzer), "Analyzer(lang='eng')")

    def test_str(self):
        analyzer = apertium.Analyzer('en')
        self.assertEqual(str(analyzer), "<Analyzer: 'eng-morph'>")


class TestGenerate(unittest.TestCase):
    def test_generator_single(self):
        generator = apertium.Generator('en')
        wordform = generator.generate('^cat<n><pl>$')
        self.assertEqual(wordform, 'cats')

    def test_generator_multiple(self):
        generator = apertium.Generator('en')
        lexical_units = generator.generate('^cat<n><pl>$ ^cat<n><pl>$')
        self.assertEqual(lexical_units, 'cats cats')

    def test_generator_bare(self):
        generator = apertium.Generator('en')        
        lexical_units = generator.generate('cat<n><pl>')
        self.assertEqual(lexical_units, 'cat<n><pl>')

    def test_generator_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            generator = apertium.Generator('spa')

    def test_single(self):
        wordform = apertium.generate('en', '^cat<n><pl>$')
        self.assertEqual(wordform, 'cats')

    def test_multiple(self):
        lexical_units = apertium.generate('en', '^cat<n><pl>$ ^cat<n><pl>$')
        self.assertEqual(lexical_units, 'cats cats')

    def test_bare(self):
        lexical_units = apertium.generate('en', 'cat<n><pl>')
        self.assertEqual(lexical_units, 'cat<n><pl>')

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            apertium.generate('spa', 'cat<n><pl>')

    def test_repr(self):
        generator = apertium.Generator('eng')
        self.assertEqual(repr(generator), "Generator(lang='eng')")

    def test_str(self):
        generator = apertium.Generator('eng')
        self.assertEqual(str(generator), "<Generator: 'eng-gener'>")


class TestTranslate(unittest.TestCase):
    def test_translator_en_spa(self):
        translator = apertium.Translator('eng', 'spa')
        translated = translator.translate('cats')
        self.assertEqual(translated, 'Gatos')

    def test_en_spa(self):
        translated = apertium.translate('eng', 'spa', 'cats')
        self.assertEqual(translated, 'Gatos')

    def test_repr(self):
        translator = apertium.Translator('eng', 'spa')
        self.assertEqual(repr(translator), "Translator(pair='eng-spa')")

    def test_str(self):
        translator = apertium.Translator('eng', 'spa')
        self.assertEqual(str(translator), "<Translator: 'en-es.mode'>")
