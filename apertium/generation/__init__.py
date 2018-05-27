from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute

if False:
    from typing import List, Union, Tuple  # noqa: F401


def preproc_text(in_text):  # type: (str) -> List[LexicalUnit]
    if len(list(parse(in_text))) == 0:
        in_text = '^%s$' % (in_text,)
        lexical_units = list(parse(in_text))
    else:
        lexical_units = list(parse(in_text))
    return lexical_units


def generate(lang, in_text, formatting='none'):  # type: (str, str, str) -> Union[str, List[str]]
    lang = to_alpha3_code(lang)

    if lang in apertium.generators:
        path, mode = apertium.generators[lang]
        commands = [['apertium', '-d', path, '-f', formatting, mode]]
        result = execute(in_text, commands)
        return result
    else:
        raise apertium.ModeNotInstalled(lang)
