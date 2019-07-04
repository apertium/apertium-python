import os
import subprocess
import tempfile
from typing import List

try:
    import apertium_core
    import lextools
    import lttoolbox
    wrapper_available = True
except ImportError:
    wrapper_available = False

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
    Executes the given list of commands and returns the final output

    Returns:
        str
    """
    end = inp.encode()
    for command in commands:
        # On Windows platform the file can't be opened once again
        # The file is first opened in python for writing and then
        # opened again with swig wrapper
        # NamedTemporaryFile gets deleted (if delete=True) upon closing,
        # so manually delete the file afterwards
        used_wrapper = True
        if wrapper_available:
            input_file = tempfile.NamedTemporaryFile(delete=False)
            output_file = tempfile.NamedTemporaryFile(delete=False)
            arg = command[1][1] if len(command) >= 3 else ''
            path = command[-1]
            input_file_name, output_file_name = input_file.name, output_file.name
            with open(input_file_name, 'w') as input_file:
                text = end.decode()
                input_file.write(text)
            if 'lt-proc' == command[0]:
                lttoolbox.LtLocale.tryToSetLocale()
                fst = lttoolbox.FST()
                if not fst.valid():
                    raise ValueError('FST Invalid')
                fst = lttoolbox.FST()
                fst.lt_proc(arg, path, input_file_name, output_file_name)
            elif 'lrx-proc' == command[0]:
                lextools.LtLocale.tryToSetLocale()
                lrx = lextools.LRX()
                lrx.lrx_proc(arg, path, input_file.name, output_file.name)
            elif 'apertium-transfer' == command[0]:
                obj = apertium_core.apertium()
                obj.transfer_text(arg, command[2], command[3], input_file.name, output_file.name)
            elif 'apertium-interchunk' == command[0]:
                obj = apertium_core.apertium()
                obj.interchunk_text(arg, command[1], command[2], input_file.name, output_file.name)
            elif 'apertium-postchunk' == command[0]:
                obj = apertium_core.apertium()
                obj.postchunk_text(arg, command[1], command[2], input_file.name, output_file.name)
            elif 'apertium-pretransfer' == command[0]:
                obj = apertium_core.apertium()
                obj.pretransfer(arg, input_file.name, output_file.name)
            else:
                used_wrapper = False
            if used_wrapper:
                with open(output_file_name) as output_file:
                    end = output_file.read().encode()
            os.remove(input_file_name)
            os.remove(output_file_name)
        if not wrapper_available or not used_wrapper:
            apertium.logger.warning('Calling subprocess %s', command[0])
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
