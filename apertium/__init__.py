from apertium.mode_search import search_path
from apertium.analysis import Analyzer, analyze  # noqa: F401
from apertium.generation import Generator, generate  # noqa: F401
from apertium.translation import Translator, translate  # noqa: F401


if False:
    from typing import List, Dict, Tuple  # noqa: F401


class ModeNotInstalled(ValueError):
    pass

class Paths(list):
    def __init__(self, elements):
        for element in elements:
            update_modes(element)
        super(Paths, self).__init__(elements)

    def extend(self, elements):
        if isinstance(elements, list):
            for element in elements:
                update_modes(element)
        else:
            update_modes(elements)
        super(Paths, self).extend(elements)

    def __add__(self, elements):
        for element in elements:
            update_modes(element)
        super(Paths, self).__add__(elements)

def update_modes(pair_path):  # type: (str) -> None
    print("running on %s", pair_path)
    modes = search_path(pair_path)
    print("these are the modes", modes)
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
    paths.append(pair_path)
    update_modes(pair_path)


analyzers = {}  # type: Dict[str, Tuple[str, str]]
generators = {}  # type: Dict[str, Tuple[str, str]]
pairs = {}  # type: Dict[str, str]
paths = Paths(['/usr/share/apertium', '/usr/local/share/apertium'])
# for path in paths:
#     update_modes(path)
