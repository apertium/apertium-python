import re

import apertium
from apertium.utils import to_alpha3_code, execute


def preproc_text(in_text):
        lexical_units = re.findall(r'(\^[^\$]*\$[^\^]*)', in_text)  # TODO: replace with streamparser
        if len(lexical_units) == 0:
            lexical_units = ['^%s$' % (in_text,)]
        return lexical_units, '[SEP]'.join(lexical_units)


def postproc_text(lexical_units, result):
    return [(generation, lexical_units[i])
            for (i, generation)
            in enumerate(result.split('[SEP]'))][0][0]


def generate(in_text, lang):
    in_mode = to_alpha3_code(lang)

    if in_mode in apertium.generators:
        [path, mode] = apertium.generators[in_mode]
        formatting = 'none'
        commands = [['apertium', '-d', path, '-f', formatting, mode]]
        lexical_units, to_generate = preproc_text(in_text)
        result = execute(to_generate, commands)
        return postproc_text(lexical_units, result)
    else:
        return None
