from apertium.mode_search import search_path
from apertium.analysis import analyze  # noqa: F401
from apertium.generation import generate  # noqa: F401
from apertium.translation import translate  # noqa: F401


if False:
    from typing import List, Dict, Tuple  # noqa: F401


class ModeNotInstalled(ValueError):
    pass


class ProcessFailure(Exception):
    pass


def update_modes(pair_path):  # type: (str) -> None
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
    pair_paths.append(pair_path)
    update_modes(pair_path)


pair_paths = ['/usr/share/apertium', '/usr/local/share/apertium']
analyzers = {}  # type: Dict[str, Tuple[str, str]]
generators = {}  # type: Dict[str, Tuple[str, str]]
pairs = {}  # type: Dict[str, str]
for pair_path in pair_paths:
    update_modes(pair_path)
