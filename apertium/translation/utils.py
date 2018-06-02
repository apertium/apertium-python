import sys

import apertium
from apertium.utils import parse_mode_file


def get_pipe_cmds(l1, l2):
    if (l1, l2) not in apertium.pipeline_cmds:
        mode_path = apertium.pairs['%s-%s' % (l1, l2)]
        apertium.pipeline_cmds[(l1, l2)] = parse_mode_file(mode_path)
    return apertium.pipeline_cmds[(l1, l2)]


def get_pair_or_error(langpair, text_length):
    try:
        l1, l2 = map(to_alpha3_code, langpair.split('|'))
    except ValueError:
        print("Pair is Invalid")
        return None
    if '%s-%s' % (l1, l2) not in apertium.pairs:
        print("Pair is not Installed")
        return None
    else:
        return (l1, l2)


def get_format(format, deformat, reformat):
    if format:
        deformat = 'apertium-des' + format
        reformat = 'apertium-re' + format
    else:
        if 'apertium-des' not in deformat:
            deformat = 'apertium-des' + deformat
        if 'apertium-re' not in reformat:
            reformat = 'apertium-re' + reformat

    return deformat, reformat