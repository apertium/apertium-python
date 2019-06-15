import re
import subprocess
from typing import List

import apertium  # noqa: F401
from apertium import lttoolbox
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
        if 'lt-proc' in command and ('-w' in command or '-g' in command):
                ltp = lttoolbox.LtProc(command, end.decode())
                end = ltp.execute()
        else:
            proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            end, _ = proc.communicate(end)
    return end.decode()


def parse_mode_file(mode_path: str) -> List[List[str]]:
    """
    Args:
        mode_path (str)

    Returns:
        List[List[str]]
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
