from apertium.mode_search import search_path
from apertium.analysis import Analyzer, analyze  # noqa: F401
from apertium.generation import Generator, generate  # noqa: F401
from apertium.translation import Translator, translate  # noqa: F401
from platform import system
from os import getenv
from os.path import join
from os.path import isdir


if False:
    from typing import List, Dict, Tuple  # noqa: F401


class ModeNotInstalled(ValueError):
    pass


def _update_modes(pair_path):  # type: (str) -> None
    """
    Args:
        pair_path (str)
    """
    modes = search_path(pair_path)
    if modes['pair']:
        for path, lang_src, lang_trg in modes['pair']:
            pairs['%s-%s' % (lang_src, lang_trg)] = path
    if modes['analyzer']:
        for dirpath, modename, lang_pair in modes['analyzer']:
            analyzers[lang_pair] = (dirpath, modename)
    if modes['generator']:
        for dirpath, modename, lang_pair in modes['generator']:
            generators[lang_pair] = (dirpath, modename)


def append_pair_path(pair_path):  # type: (str) -> None
    """
    Args:
        pair_path (str)
    """
    pair_paths.append(pair_path)
    _update_modes(pair_path)


def append_pair_path_windows():
    if system() == 'Windows':
        install_path = getenv('LOCALAPPDATA')
        apertium_lang_path = \
            join(install_path, 'apertium-all-dev', 'share', 'apertium')
        if isdir(apertium_lang_path):
            append_pair_path(apertium_lang_path)


pair_paths = ['/usr/share/apertium', '/usr/local/share/apertium']
analyzers = {}  # type: Dict[str, Tuple[str, str]]
generators = {}  # type: Dict[str, Tuple[str, str]]
pairs = {}  # type: Dict[str, str]
for pair_path in pair_paths:
    _update_modes(pair_path)
append_pair_path_windows()
