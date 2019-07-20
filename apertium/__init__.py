import logging
import os
import platform
from typing import Dict, Tuple

from apertium.analysis import analyze, Analyzer  # noqa: F401
from apertium.generation import generate, Generator  # noqa: F401
from apertium.installer import install_language_pack  # noqa: F401
from apertium.mode_search import search_path
from apertium.translation import translate, Translator  # noqa: F401


class ModeNotInstalled(ValueError):
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


def append_pair_path(pair_path: str) -> None:
    """
    Args:
        pair_path (str)
    """
    pair_paths.append(pair_path)
    _update_modes(pair_path)


def append_pair_path_windows() -> None:
    if platform.system() == 'Windows':
        install_path = os.getenv('LOCALAPPDATA')
        if install_path:
            apertium_lang_path = \
                os.path.join(install_path, 'apertium-all-dev', 'share', 'apertium')
            if os.path.isdir(apertium_lang_path):
                append_pair_path(apertium_lang_path)


def update_path_windows() -> None:
    """Adding the Apertium Binaries to Process' PATH"""

    if platform.system() == 'Windows':
        install_path = os.environ['LOCALAPPDATA']
        current = os.environ['path']

        apertium_path = os.path.join(install_path, 'apertium-all-dev', 'bin')
        if os.path.isdir(apertium_path):
            update_path = '{}{}{}{}'.format(current, os.pathsep, apertium_path, os.pathsep)
            os.environ['path'] = update_path


pair_paths = ['/usr/share/apertium', '/usr/local/share/apertium']
analyzers = {}  # type: Dict[str, Tuple[str, str]]
generators = {}  # type: Dict[str, Tuple[str, str]]
pairs = {}  # type: Dict[str, str]
for pair_path in pair_paths:
    _update_modes(pair_path)
append_pair_path_windows()
update_path_windows()
logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger()
