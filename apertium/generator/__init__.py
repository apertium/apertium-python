import streamparser
from typing import List, Union, Tuple

import apertium
from apertium.utils import to_alpha3_code, execute

CONST_SEP = '[SEP]'


def preproc_text(in_text: str) -> Tuple[List[str], str]:
        if len(list(streamparser.parse(in_text))) == 0:
            lexical_units = ['^%s$' % (in_text,)]
        return lexical_units, CONST_SEP.join(lexical_units)


def postproc_text(lexical_units: List[str], result: str) -> str:
    return [(generation, lexical_units[i])
            for (i, generation)
            in enumerate(result.split(CONST_SEP))][0][0]


def generate(in_text: str, lang: str)-> Union[str, List[str], Exception]:
    in_mode = to_alpha3_code(lang)

    if in_mode in apertium.generators:
        [path, mode] = apertium.generators[in_mode]
        formatting = 'none'
        commands = [['apertium', '-d', path, '-f', formatting, mode]]
        lexical_units, to_generate = preproc_text(in_text)
        result = execute(to_generate, commands)
        return postproc_text(lexical_units, result)
    else:
        raise Exception('mode not installed')
