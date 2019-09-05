__author__ = 'Lokendra Singh, Arghya Bhatttacharya, Sushain K. Cherivirala, Andi Qu'
__license__ = 'GNU General Public License v3.0'
__version__ = '0.1.0'

import logging
import os
import platform
from typing import Dict, Tuple

from apertium.analysis import analyze, Analyzer  # noqa: F401
from apertium.generation import generate, Generator  # noqa: F401
from apertium.installer import install_module  # noqa: F401
from apertium.mode_search import search_path
from apertium.tagger import tag, Tagger  # noqa: F401
from apertium.translation import translate, Translator  # noqa: F401
from apertium.utils import wrappers_available  # noqa: F401


class ModeNotInstalled(ValueError):
    pass


class InstallationNotSupported(ValueError):
    pass


def _update_modes(pair_path: str) -> None:
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
    if modes['tagger']:
        for dirpath, modename, lang_pair in modes['tagger']:
            taggers[lang_pair] = (dirpath, modename)


def append_pair_path(pair_path: str) -> None:
    """
    Args:
        pair_path (str)
    """
    pair_paths.append(pair_path)
    _update_modes(pair_path)


def append_pair_path_windows() -> None:
    try:
        install_path = os.environ['LOCALAPPDATA']
        if install_path:
            apertium_lang_path = \
                os.path.join(install_path, 'apertium-all-dev', 'share', 'apertium')
            if os.path.isdir(apertium_lang_path):
                append_pair_path(apertium_lang_path)
    except KeyError:
        print('This function is available only for Windows')
        raise InstallationNotSupported(platform.system())


def update_path_windows() -> None:
    """Adding the Apertium Binaries to shell PATH"""

    try:
        install_path = os.environ['LOCALAPPDATA']
        current = os.environ['PATH']

        apertium_path = os.path.join(install_path, 'apertium-all-dev', 'bin')
        if os.path.isdir(apertium_path):
            update_path = '{}{}{}{}'.format(current, os.pathsep, apertium_path, os.pathsep)
            os.environ['PATH'] = update_path

    except KeyError:
        print('This function is available only for Windows')
        raise InstallationNotSupported(platform.system())


pair_paths = ['/usr/share/apertium', '/usr/local/share/apertium']
analyzers = {}  # type: Dict[str, Tuple[str, str]]
generators = {}  # type: Dict[str, Tuple[str, str]]
taggers = {}  # type: Dict[str, Tuple[str, str]]
pairs = {}  # type: Dict[str, str]
for pair_path in pair_paths:
    _update_modes(pair_path)
if platform.system() == 'Windows':
    append_pair_path_windows()
    update_path_windows()
logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger()
