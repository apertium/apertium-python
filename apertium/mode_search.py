import os
import re
from typing import Dict, List, Tuple, Union  # noqa: F401

from apertium.utils import to_alpha3_code


def is_loop(dirpath: str, rootpath: str, real_root: (Union[None, str]) = None) -> bool:
    """
    Args:
        dirpath (str)
        rootpath (str)
        real_root (Union[None, str])

    Returns:
        bool
    """
    if os.path.islink(dirpath):
        # We just descended into a directory via a symbolic link
        # Check if we're referring to a directory that is
        # a parent of our nominal directory

        if not real_root:
            real_root = os.path.abspath(os.path.realpath(rootpath))

        relative = os.path.relpath(dirpath, rootpath)
        nominal_path = os.path.join(real_root, relative)
        real_path = os.path.abspath(os.path.realpath(dirpath))

        for nominal, real in zip(nominal_path.split(os.sep),
                                 real_path.split(os.sep)):
            if nominal != real:
                return False
        else:
            return True
    else:
        return False


def search_path(rootpath: str, include_pairs: bool = True) -> Dict[str, List[Tuple[str, str, str]]]:
    """
    Args:
        rootpath (str)
        include_pairs (bool)

    Returns:
        Dict[str, List[Tuple[str, str, str]]]
    """
    lang_code = r'[a-z]{2,3}(?:_[A-Za-z]+)?'
    type_re = {
        'analyzer': re.compile(r'(({0}(-{0})?)-(an)?mor(ph)?)\.mode'.format(lang_code)),
        'generator': re.compile(r'(({0}(-{0})?)-gener[A-z]*)\.mode'.format(lang_code)),
        'pair': re.compile(r'({0})-({0})\.mode'.format(lang_code)),
    }
    modes = {
        'analyzer': [],
        'generator': [],
        'pair': [],
    }  # type: Dict[str, List[Tuple[str, str, str]]]

    real_root = os.path.abspath(os.path.realpath(rootpath))

    for dirpath, dirnames, files in os.walk(rootpath, followlinks=True):
        if is_loop(dirpath, rootpath, real_root):
            dirnames[:] = []
            continue
        for filename in [f for f in files if f.endswith('.mode')]:
            for mtype, regex in type_re.items():
                m = regex.match(filename)
                if m:
                    if mtype != 'pair':
                        modename = m.group(1)  # e.g. en-es-anmorph
                        langlist = [to_alpha3_code(l) for l in m.group(2).split('-')]
                        lang_pair = '-'.join(langlist)  # e.g. en-es
                        dir_of_modes = os.path.dirname(dirpath)
                        mode = (dir_of_modes,
                                modename,
                                lang_pair)
                        modes[mtype].append(mode)
                    elif include_pairs:
                        lang_src, lang_trg = m.groups()
                        mode = (os.path.join(dirpath, filename),
                                to_alpha3_code(lang_src),
                                to_alpha3_code(lang_trg))
                        modes[mtype].append(mode)
    return modes
