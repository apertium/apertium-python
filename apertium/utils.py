import subprocess
import typing  # noqa:F401
from typing import List

from apertium.iso639 import iso_639_codes

iso639_codes_inverse = {v: k for k, v in iso_639_codes.items()}


def to_alpha3_code(code: str) -> str:
    if '_' in code:
        code, variant = code.split('_')
        return '%s_%s' % ((iso639_codes_inverse[code], variant) if code in iso639_codes_inverse else (code, variant))
    else:
        return iso639_codes_inverse[code] if code in iso639_codes_inverse else code


def execute(inp: str, commands: List[List[str]]) -> str:
    procs = []
    end = inp.encode()
    for i, command in enumerate(commands):
        procs.append(
            subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE),
        )
        end, _ = procs[i].communicate(end)
    return end.decode()
