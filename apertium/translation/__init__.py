import re
import subprocess  # noqa: F401
from subprocess import Popen, PIPE

if False:
    from typing import List, Dict, Tuple, Union, Optional, NamedTuple  # noqa: F401

import apertium  # noqa: F401
from apertium.utils import to_alpha3_code, execute, parse_mode_file, ParsedModes  # noqa: F401


def get_pipe_cmds(l1, l2):  # type: (str, str) -> ParsedModes
    if (l1, l2) not in apertium.pipeline_cmds:
        mode_path = apertium.pairs['%s-%s' % (l1, l2)]
        apertium.pipeline_cmds[(l1, l2)] = parse_mode_file(mode_path)  # type: ignore
    return apertium.pipeline_cmds[(l1, l2)]


def get_pair_or_error(l1, l2):  # type: (str, str) -> Union[None, Tuple[str, str]]
    try:
        l1, l2 = map(to_alpha3_code, [l1, l2])
    except ValueError:
        print('Pair is Invalid')
        return None
    if '%s-%s' % (l1, l2) not in apertium.pairs:
        print('Pair is not Installed')
        return None
    else:
        return (l1, l2)


def get_format(format, deformat, reformat):  # type: (Union[str, None], Union[str, None], Union[str, None]) -> Tuple[Union[str, None], Union[str, None]]
    if format:
        deformat = 'apertium-des' + format
        reformat = 'apertium-re' + format
    else:
        if 'apertium-des' not in deformat:  # type: ignore
            deformat = 'apertium-des' + deformat  # type: ignore
        if 'apertium-re' not in reformat:  # type: ignore
            reformat = 'apertium-re' + reformat  # type: ignore

    return deformat, reformat


def check_ret_code(name, proc):  # type: (str, subprocess.Popen) -> None
    if proc.returncode != 0:
        raise apertium.ProcessFailure('%s failed, exit code %s', name, proc.returncode)


def validate_formatters(deformat, reformat):  # type: (Union[str, None], Union[str, None]) -> Tuple[Union[str, object], Union[str, object]]
    def valid1(elt, lst):  # type: (Union[str, None], List[object]) -> Union[str, object]
        if elt in lst:
            return elt
        else:
            return lst[0]
    # First is fallback:
    deformatters = [
        'apertium-deshtml',
        'apertium-destxt',
        'apertium-desrtf',
        False]
    reformatters = [
        'apertium-rehtml-noent',
        'apertium-rehtml',
        'apertium-retxt',
        'apertium-rertf',
        False]
    return valid1(deformat, deformatters), valid1(reformat, reformatters)


def get_deformat(deformat, text):  # type: (str, str) -> str
    if deformat:
        proc_deformat = Popen(deformat, stdin=PIPE, stdout=PIPE)
        proc_deformat.stdin.write(bytes(text, 'utf-8'))
        deformatted = proc_deformat.communicate()[0]
        deformatted = deformatted.decode()
        check_ret_code('Deformatter', proc_deformat)
    else:
        deformatted = bytes(text, 'utf-8')
    deformatted = str(deformatted)
    return deformatted  # type: ignore


def get_reformat(reformat, text):  # type: (str, str) -> str
    if reformat:
        proc_reformat = Popen(reformat, stdin=PIPE, stdout=PIPE)
        proc_reformat.stdin.write(bytes(text, 'utf-8'))
        result = proc_reformat.communicate()[0]
        check_ret_code('Reformatter', proc_reformat)
    else:
        result = re.sub(rb'\0$', b'', text)  # type: ignore
    return result  # type: ignore


def translate(
        l1,
        l2,
        text,
        markunknown='no',
        format=None,
        deformat='txt',
        reformat='txt'):  # type: (str, str, str, str, Union[str, None], str, str) -> str
    pair = get_pair_or_error(l1, l2)
    if pair is not None:
        (l1, l2) = pair
        cmds = list(get_pipe_cmds(l1, l2).commands)
        unsafe_deformat, unsafe_reformat = get_format(
            format, deformat, reformat)
        deformat, reformat = validate_formatters(  # type: ignore
            unsafe_deformat, unsafe_reformat)
        deformatted = get_deformat(deformat, text)
        output = execute(deformatted, cmds)
        result = get_reformat(reformat, output).strip()
        return result.decode()  # type: ignore
    else:
        raise apertium.PairNotInstalled()
