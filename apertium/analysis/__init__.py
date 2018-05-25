import streamparser  # noqa: F401
from streamparser import parse

import apertium
from apertium.utils import to_alpha3_code, execute

if False:
    from typing import List, Union  # noqa: F401


def postproc_text(result):
    # type: (str) -> List[streamparser.LexicalUnit]

    """
    postprocesses the input
    """
    lexical_units = list(parse(result))
    return lexical_units


def analyze(in_text, lang, formatting='txt'):
    # type: (str, str, str) -> List[streamparser.LexicalUnit]
    """
    runs apertium to analyze the input
    """
    in_mode = to_alpha3_code(lang)

    if in_mode in apertium.analyzers:
        path, mode = apertium.analyzers[in_mode]
        commands = [['apertium', '-d', path, '-f', formatting, mode]]
        result = execute(in_text, commands)
        return postproc_text(result)
    else:
        raise apertium.ModeNotInstalled(in_mode)
