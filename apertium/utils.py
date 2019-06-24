import os
import subprocess
import tempfile
from typing import List

import lextools
import lttoolbox

import apertium  # noqa: F401
from apertium.iso639 import iso_639_codes

iso639_codes_inverse = {v: k for k, v in iso_639_codes.items()}


def to_alpha3_code(code: str) -> str:
    """
    Args:
        code (str)

    Returns:
        str
    """
    if '_' in code:
        code, variant = code.split('_')
        return '%s_%s' % ((iso639_codes_inverse[code], variant) if code in iso639_codes_inverse else (code, variant))
    else:
        return iso639_codes_inverse[code] if code in iso639_codes_inverse else code


def execute_pipeline(inp: str, commands: List[List[str]]) -> str:
    """
    Args:
        inp (str)
        commands (List[List[str]])

    Returns:
        str
    """
    end = inp.encode()
    for command in commands:
        lttoolbox.LtLocale.tryToSetLocale()
        input_file = tempfile.NamedTemporaryFile('w', delete=False)
        output_file = tempfile.NamedTemporaryFile('r', delete=False)
        arg = command[1][1] if len(command) == 3 else ''
        path = command[-1]
        wrapper_flag = True
        input_file_name, output_file_name = input_file.name, output_file.name
        with open(input_file_name, 'w') as input_file:
            text = end.decode()
            input_file.write(text)
        if 'lt-proc' == command[0]:
            fst = lttoolbox.FST()
            if not fst.valid():
                raise ValueError('FST Invalid')
            fst = lttoolbox.FST()
            fst.lt_proc(arg, path, input_file_name, output_file_name)
        elif 'lrx-proc' == command[0]:
            lrx = lextools.LRX()
            lrx.lrx_proc(arg, path, input_file.name, output_file.name)
        else:
            apertium.logger.warning('Calling subprocess %s', command[0])
            proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            end, _ = proc.communicate(end)
            wrapper_flag = False
        if wrapper_flag:
            with open(output_file_name) as output_file:
                end = output_file.read().encode()
        os.remove(input_file_name)
        os.remove(output_file_name)
    return end.decode()


def parse_mode_file(mode_path: str) -> List[List[str]]:
    """
    Args:
        mode_path (str)

    Returns:
        List[List[str]]
    """
    with open(mode_path) as mode_file:
        mode_str = mode_file.read().strip()
    if mode_str:
        commands = []
        for cmd in mode_str.strip().split('|'):
            # TODO: we should make language pairs install
            # modes.xml instead; this is brittle (what if a path
            # has | or ' in it?)
            cmd = cmd.replace('$2', '').replace('$1', '-g')
            commands.append([c.strip("'") for c in cmd.split()])
        return commands
    else:
        raise apertium.ModeNotInstalled(mode_path)
