import importlib.util
import os
import platform
import shutil
import sys
from typing import Dict, Tuple
import unittest

from streamparser import known, SReading

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_path)

import apertium  # noqa: E402


class TestApertiumInit(unittest.TestCase):
    def test_append_pair_path(self):
        apertium.pair_paths = []
        apertium.analyzers = {}  # type: Dict[str, Tuple[str, str]]
        apertium.generators = {}  # type: Dict[str, Tuple[str, str]]
        apertium.taggers = {}  # type: Dict[str, Tuple[str, str]]
        apertium.pairs = {}  # type: Dict[str, str]
        apertium.append_pair_path('/usr/share/apertium')
        apertium.append_pair_path('/usr/local/share/apertium')
        apertium.append_pair_path_windows()
        if not apertium.pair_paths or not apertium.analyzers or not apertium.generators or not apertium.taggers or not apertium.pairs:
            self.fail('Pair Paths not added to the list/dictionary')


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

    @unittest.skipIf(platform.system() == 'Windows', 'apertium binaries not available for windows')
    def test_install_apertium_linux(self):
        apertium.installer.install_apertium_linux()
        apertium_processes = ['apertium-anaphora',
                             ]
        for process in apertium_processes:
            self.assertIsNotNone(shutil.which(process), 'apertium linux installer not working. {} not available on system path'.format(process))
            break

    def test_install_module(self):
        language = 'kir'
        apertium.installer.install_module(language)
        importlib.reload(apertium)
        self.assertIn(language, apertium.analyzers, 'apetium.install_module not working')

    @unittest.skipIf(platform.system() == 'Windows', 'wrappers not available for windows')
    def test_install_wrapper(self):
        apertium.installer.install_wrapper('python3-lttoolbox')
        if platform.system() == 'Linux':
            sys.path.append('/usr/lib/python3/dist-packages')
        self.assertIsNotNone(importlib.util.find_spec('lttoolbox'), 'Wrapper not installed')


class TestSubProcess(unittest.TestCase):
    def test_analyze_en_subprocess(self):
        apertium.utils.wrappers_available = False
        test_analyze = TestAnalyze()
        test_analyze.test_analyzer_en()
        test_analyze.test_analyze_en()
        apertium.utils.wrappers_available = True

    def test_generate_en_subprocess(self):
        apertium.utils.wrappers_available = False
        test_generate = TestGenerate()
        test_generate.test_generator_single()
        test_generate.test_generator_multiple()
        test_generate.test_generator_bare()
        test_generate.test_single()
        test_generate.test_multiple()
        test_generate.test_bare()
        apertium.utils.wrappers_available = True

    def test_translate_en_es_subprocess(self):
        apertium.utils.wrappers_available = False
        test_translate = TestTranslate()
        test_translate.test_translator_en_spa()
        test_translate.test_en_spa()
        apertium.utils.wrappers_available = True

    def test_tagger_en_subprocess(self):
        apertium.utils.wrappers_available = False
        test_tagger = TestTagger()
        test_tagger.test_tagger_en()
        test_tagger.test_tag_en()
        apertium.utils.wrappers_available = True


class TestTranslate(unittest.TestCase):
    @unittest.skipIf(platform.system() == 'Windows', 'lrx-proc -m bug #25')
    def test_translator_en_spa(self):
        translator = apertium.Translator('eng', 'spa')
        translated = translator.translate('cats')
        self.assertEqual(translated, 'Gatos')

    @unittest.skipIf(platform.system() == 'Windows', 'lrx-proc -m bug #25')
    def test_en_spa(self):
        translated = apertium.translate('eng', 'spa', 'cats')
        self.assertEqual(translated, 'Gatos')

    @unittest.skipIf(platform.system() == 'Windows', 'lrx-proc -m bug #25')
    def test_en_spa_formatting(self):
        translated = apertium.translate('eng', 'spa', 'cats', formatting='txt')
        self.assertEqual(translated, 'Gatos')

    def test_kaz_tat(self):
        translated = apertium.translate('kaz', 'tat', 'мысық')
        self.assertEqual(translated, 'мәче')

    def test_kaz_tat_formatting(self):
        translated = apertium.translate('kaz', 'tat', 'мысық', formatting='txt')
        self.assertEqual(translated, 'мәче')

    def test_translator_kaz_tat(self):
        translator = apertium.Translator('kaz', 'tat')
        translated = translator.translate('мысық')
        self.assertEqual(translated, 'мәче')


class TestTagger(unittest.TestCase):
    def test_tagger_en(self):
        tagger = apertium.Tagger('en')
        lexical_units = tagger.tag('cats')
        lexical_unit = lexical_units[0]
        self.assertListEqual(lexical_unit.readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

    def test_tag_en(self):
        lexical_units = apertium.tag('eng', 'cats')
        lexical_unit = lexical_units[0]
        self.assertListEqual(lexical_unit.readings, [[SReading(baseform='cat', tags=['n', 'pl'])]])
        self.assertEqual(lexical_unit.wordform, 'cats')
        self.assertEqual(lexical_unit.knownness, known)

    def test_uninstalled_mode(self):
        with self.assertRaises(apertium.ModeNotInstalled):
            apertium.Tagger('spa')
