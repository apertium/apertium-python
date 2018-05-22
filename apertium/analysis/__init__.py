from streamparser import parse

import apertium
from apertium.utils import to_alpha3_code, execute


def postproc_text(result):
    """
    postprocesses the input
    """
    lexical_units = parse(result)
    return list(lexical_units)[0]


def analyze(in_text, lang):
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
