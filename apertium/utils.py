import subprocess
import re
from collections import namedtuple


from apertium.iso639 import iso_639_codes

if False:
    import typing # noqa:F401
    from typing import List # noqa:F401

iso639_codes_inverse = {v: k for k, v in iso_639_codes.items()}


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

def cmd_needs_z(cmd):
    exceptions = r'^\s*(vislcg3|cg-mwesplit|hfst-tokeni[sz]e|divvun-suggest)'
    return re.match(exceptions, cmd) is None

ParsedModes = namedtuple('ParsedModes', 'do_flush commands')

def parse_mode_file(mode_path):
    mode_str = open(mode_path, 'r').read().strip()
    if mode_str:
        if 'ca-oc@aran' in mode_str:
            do_flush = False
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
            do_flush = True
            commands = []
            for cmd in mode_str.strip().split('|'):
                # TODO: we should make language pairs install
                # modes.xml instead; this is brittle (what if a path
                # has | or ' in it?)
                cmd = cmd.replace('$2', '').replace('$1', '-g')
                if cmd_needs_z(cmd):
                    cmd = re.sub(r'^\s*(\S*)', r'\g<1> -z', cmd)
                commands.append([c.strip("'")
                                 for c in cmd.split()])
        return ParsedModes(do_flush, commands)
    else:
        raise Exception('Could not parse mode file %s', mode_path)