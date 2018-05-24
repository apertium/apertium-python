import streamparser
from streamparser import parse
from typing import List, Union

import apertium
from apertium.utils import to_alpha3_code, execute


def postproc_text(result: str) -> List[streamparser.LexicalUnit]:
    """
    postprocesses the input
    """
    lexical_units = list(parse(result))
    lexical_units.pop()
    return lexical_units


def analyze(in_text: str, lang: str) -> Union[List[streamparser.LexicalUnit], Exception]:
    """
    runs apertium to analyze the input
    """
    in_mode = to_alpha3_code(lang)

    if in_mode in apertium.analyzers:
        path, mode = apertium.analyzers[in_mode]
        formatting = 'txt'
        commands = [['apertium', '-d', path, '-f', formatting, mode]]
        result = execute(in_text, commands)
        return postproc_text(result)
    else:
        raise Exception('mode not installed')
