import streamparser  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute

if False:
    from typing import List, Union, Tuple  # noqa: F401

SEPARATOR = '[SEP]'


def preproc_text(in_text):  # type: (str) -> Tuple[List[str], str]
    if len(list(streamparser.parse(in_text))) == 0:
        lexical_units = ['^%s$' % (in_text,)]
    return lexical_units, SEPARATOR.join(lexical_units)


def postproc_text(lexical_units, result):  # type: (List[str], str) -> str
    return [(generation, lexical_units[i])
            for (i, generation)
            in enumerate(result.split(SEPARATOR))][0][0]


def generate(in_text, lang, formatting='none'):  # type: (str, str, str) -> Union[str, List[str]]
    lang = to_alpha3_code(lang)

    if lang in apertium.generators:
        path, mode = apertium.generators[lang]
        commands = [['apertium', '-d', path, '-f', formatting, mode]]
        lexical_units, to_generate = preproc_text(in_text)
        result = execute(to_generate, commands)
        return postproc_text(lexical_units, result)
    else:
        raise apertium.ModeNotInstalled(lang)
