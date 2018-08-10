#!/usr/bin/env python3
# coding=utf-8
"""
Usage: import apertium
"""

__all__ = [
    'Knownness', 'known', 'unknown', 'biunknown', 'genunknown', 'LexicalUnit', 'SReading',
    'subreading_to_string', 'reading_to_string', 'mainpos', 'parse', 'parse_file',
]
__author__ = 'Arghya Bhattacharya, Sushain K. Cherivirala'
__copyright__ = ''
__credits__ = ['Arghya Bhattacharya', 'Sushain K. Cherivirala']
__license__ = 'GPLv3+'
__status__ = 'Development'
__version__ = '1.0.0'


from apertium.mode_search import search_path
from apertium.analysis import Analyzer, analyze  # noqa: F401
from apertium.generation import Generator, generate  # noqa: F401
from apertium.translation import Translator, translate  # noqa: F401


if False:
    from typing import List, Dict, Tuple  # noqa: F401


class ModeNotInstalled(ValueError):
    """The specific mode that is required to run the following operation \n
    doesn't exist in the given paths
    """
    pass


def update_modes(path):  # type: (str) -> None
    """Updates the pairs, analyzers, generator dictionaries with entries of the installed modes \n

    Args:
        path (str): A string that is the absolute location to the modes to be added.
    """
    modes = search_path(path)
    if modes['pair']:
        for path, lang_src, lang_trg in modes['pair']:
            pairs['%s-%s' % (lang_src, lang_trg)] = path
    if modes['analyzer']:
        for dirpath, modename, lang_pair in modes['analyzer']:
            analyzers[lang_pair] = (dirpath, modename)
    if modes['generator']:
        for dirpath, modename, lang_pair in modes['generator']:
            generators[lang_pair] = (dirpath, modename)


def append_pair_path(path):  # type: (str) -> None
    paths.append(path)
    update_modes(path)


paths = ['/usr/share/apertium', '/usr/local/share/apertium', r'..\apertium-all-dev\share\apertium']
analyzers = {}  # type: Dict[str, Tuple[str, str]]
generators = {}  # type: Dict[str, Tuple[str, str]]
pairs = {}  # type: Dict[str, str]
for path in paths:
    update_modes(path)
