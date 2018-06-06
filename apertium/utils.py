import subprocess
import re
import os

from collections import namedtuple

if False:
    from typing import List, Dict, Tuple, Union  # noqa: F401

from apertium.iso639 import iso_639_codes  # noqa: F401


iso639_codes_inverse = {v: k for k, v in iso_639_codes.items()}


ParsedModes = namedtuple('ParsedModes', 'commands')


def to_alpha3_code(code):  # type: (str) -> str
    if '_' in code:
        code, variant = code.split('_')
        return '%s_%s' % ((iso639_codes_inverse[code], variant) if code in iso639_codes_inverse else (code, variant))
    else:
        return iso639_codes_inverse[code] if code in iso639_codes_inverse else code


def execute(inp, commands):  # type: (str, List[List[str]]) -> str
    procs = []
    end = inp.encode()
    for i, command in enumerate(commands):
        procs.append(
            subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE),
        )
        end, _ = procs[i].communicate(end)
    return end.decode()


def parse_mode_file(mode_path):  # type: (str) -> ParsedModes
    mode_str = open(mode_path, 'r').read().strip()
    if mode_str:
        if 'ca-oc@aran' in mode_str:
            modes_parentdir = os.path.dirname(os.path.dirname(mode_path))
            mode_name = os.path.splitext(os.path.basename(mode_path))[0]
            commands = [[
                'apertium',
                '-f', 'html-noent',
                # Get the _parent_ dir of the mode file:
                '-d', modes_parentdir,
                mode_name,
            ]]
        else:
            commands = []
            for cmd in mode_str.strip().split('|'):
                # TODO: we should make language pairs install
                # modes.xml instead; this is brittle (what if a path
                # has | or ' in it?)
                cmd = cmd.replace('$2', '').replace('$1', '-g')
                cmd = re.sub(r'^\s*(\S*)', r'\g<1> -z', cmd)
                commands.append([c.strip("'") for c in cmd.split()])
        return ParsedModes(commands)
    else:
        raise Exception('Could not parse mode file %s', mode_path)
