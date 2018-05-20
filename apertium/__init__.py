from apertium.modesearch import search_path
from apertium.analysis import analyze  # noqa: F401
from apertium.generator import generate  # noqa: F401


def update_modes(pair_path):
    modes = search_path(pair_path)
    if len(modes['analyzer']) is not 0:
            for dirpath, modename, lang_pair in modes['analyzer']:
                analyzers[lang_pair] = (dirpath, modename)
    if len(modes['generator']) is not 0:
            for dirpath, modename, lang_pair in modes['generator']:
                generators[lang_pair] = (dirpath, modename)


def append_pair_path(pair_path):
    pair_paths.append(pair_path)
    update_modes(pair_path)


pair_paths = ['/usr/share/apertium', '/usr/local/share/apertium']
analyzers = {}
generators = {}
for pair_path in pair_paths:
    update_modes(pair_path)
