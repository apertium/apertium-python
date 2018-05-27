from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute

if False:
    from typing import List, Union  # noqa: F401


def postproc_text(result):  # type: (str) -> List[LexicalUnit]
    """
    postprocesses the input
    """
    lexical_units = list(parse(result))
    return lexical_units


def analyze(lang, in_text, formatting='txt'):  # type: (str, str, str) -> List[LexicalUnit]
    """
    runs apertium to analyze the input
    """
    lang = to_alpha3_code(lang)

    if lang in apertium.analyzers:
        path, mode = apertium.analyzers[lang]
        commands = [['apertium', '-d', path, '-f', formatting, mode]]
        result = execute(in_text, commands)
        return postproc_text(result)
    else:
        raise apertium.ModeNotInstalled(lang)
