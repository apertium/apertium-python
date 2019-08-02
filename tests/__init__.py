import importlib.util
import os
import platform
import shutil
import sys
import unittest

from streamparser import known, SReading

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
            apertium.Analyzer('spa')


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
        generator = apertium.Generator('spa')
        with self.assertRaises(apertium.ModeNotInstalled):
            generator.generate('cat<n><pl>')

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


class TestInstallation(unittest.TestCase):
    def test_apertium_installer(self):
        # This test doesn't remove existing apertium binaries.
        # So it is possible that apertium.installer.install_apertium() isn't working
        apertium.installer.install_apertium()
        apertium_processes = ['apertium-destxt', 'apertium-interchunk', 'apertium-postchunk',
                              'apertium-pretransfer', 'apertium-tagger', 'apertium-transfer',
                              'lrx-proc', 'lt-proc'
                              ]
        for process in apertium_processes:
            self.assertIsNotNone(shutil.which(process), 'apertium installer not working. {} not available on system path'.format(process))
            break

    def test_install_module(self):
        language = 'kir'
        apertium.installer.install_module(language)
        importlib.reload(apertium)
        self.assertIn(language, apertium.analyzers, 'apetium.install_module not working')

    def test_install_wrapper(self):
        apertium.installer.install_wrapper('python3-lttoolbox')
        if platform.system() == 'Linux':
            sys.path.append('/usr/lib/python3/dist-packages')
        self.assertIsNotNone(importlib.util.find_spec('lttoolbox'), 'Wrapper not installed')


class TestTranslate(unittest.TestCase):
    def test_translator_en_spa(self):
        translator = apertium.Translator('eng', 'spa')
        translated = translator.translate('cats')
        self.assertEqual(translated, 'Gatos')

    def test_en_spa(self):
        translated = apertium.translate('eng', 'spa', 'cats')
        self.assertEqual(translated, 'Gatos')
