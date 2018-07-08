import subprocess
import re

if False:
    from typing import List, Dict, Tuple, Union  # noqa: F401

import apertium  # noqa: F401
from apertium.iso639 import iso_639_codes  # noqa: F401


iso639_codes_inverse = {v: k for k, v in iso_639_codes.items()}


def to_alpha3_code(code):  # type: (str) -> str
    if '_' in code:
        code, variant = code.split('_')
        return '%s_%s' % ((iso639_codes_inverse[code], variant) if code in iso639_codes_inverse else (code, variant))
    else:
        return iso639_codes_inverse[code] if code in iso639_codes_inverse else code


def execute(inp, commands):  # type: (str, List[List[str]]) -> str
    """
    exectues the commands in a pipeline fashion and returns the output
    """
    procs = []
    end = inp.encode()
    for i, command in enumerate(commands):
        procs.append(
            subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE),
        )
        end, _ = procs[i].communicate(end)
    return end.decode()


def parse_mode_file(mode_path):  # type: (str) -> List[List[str]]
    """
    parses the modefile and returns the commands to execute for a gives mode
    """
    mode_str = open(mode_path, 'r').read().strip()
    if mode_str:
        commands = []
        for cmd in mode_str.strip().split('|'):
            # TODO: we should make language pairs install
            # modes.xml instead; this is brittle (what if a path
            # has | or ' in it?)
            cmd = cmd.replace('$2', '').replace('$1', '-g')
            cmd = re.sub(r'^\s*(\S*)', r'\g<1> -z', cmd)
            commands.append([c.strip("'") for c in cmd.split()])
        return commands
    else:
        raise apertium.ModeNotInstalled(mode_path)
