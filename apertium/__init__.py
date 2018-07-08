from apertium.mode_search import search_path
from apertium.analysis import Analyzer, analyze  # noqa: F401
from apertium.generation import Generator, generate  # noqa: F401
from apertium.translation import Translator, translate  # noqa: F401


if False:
    from typing import List, Dict, Tuple  # noqa: F401


class ModeNotInstalled(ValueError):
    pass


def update_modes(path):  # type: (str) -> None
    """
    takes a path as input and returns updates the installed modes
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


def append_path(path):  # type: (str) -> None
    paths.append(path)
    update_modes(path)


paths = ['/usr/share/apertium', '/usr/local/share/apertium']
analyzers = {}  # type: Dict[str, Tuple[str, str]]
generators = {}  # type: Dict[str, Tuple[str, str]]
pairs = {}  # type: Dict[str, str]
for path in paths:
    update_modes(path)
