import sys

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file


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


def maybe_strip_marks(mark_unknown, pair, translated):
        if mark_unknown:
            return translated
        else:
            return re.sub(self.unknown_mark_re, r'\1', translated)

def translate(langpair, text, markUnknown='no', format=None, deformat='txt', reformat='txt'):
    pair = get_pair_or_error(langpair, len(text))
    if pair is not None:
        (l1, l2) = pair
        cmds = list(get_pipe_cmds(l1, l2).commands)
        deformat, reformat = get_format(format, deformat, reformat)
        res = execute(text, cmds)
        val = maybe_strip_marks(markUnknown, pair, res)
        return res
        