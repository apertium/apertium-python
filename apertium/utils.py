import os
import platform
import subprocess
import sys
import tempfile
from typing import List

try:
    if platform.system() == 'Linux':
        sys.path.append('/usr/lib/python3/dist-packages')

    import apertium_core
    import lextools
    import lttoolbox
    import constraint_grammar
    wrappers_available = True
except ImportError:
    wrappers_available = False

import apertium  # noqa: F401
from apertium.iso639 import iso_639_codes

iso639_codes_inverse = {v: k for k, v in iso_639_codes.items()}
escape_chars = b'[]{}?^$@\\'
special_chars_map = {i: '\\' + chr(i) for i in escape_chars}


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


def deformatter(text: str) -> str:
    """
    This function is a text format processor. Data should be passed
    through this processor before being piped to lt-proc.
    """
    return '{}[][\n]'.format(text.translate(special_chars_map))


def execute_pipeline(inp: str, commands: List[List[str]]) -> str:
    """
    Executes the given list of commands and returns the final output

    Returns:
        str
    """
    end = inp.encode()
    for command in commands:
        # On Windows, a NamedTemporaryFile with delete=True can only be opened once.
        # Since the file is opened both by Python and the C++ SWIG wrappers, we use
        # delete=False and manually delete the file.
        used_wrapper = True
        if wrappers_available:
            if 'apertium-destxt' == command[0]:
                output = deformatter(end.decode())
                end = output.encode()
                continue
            input_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
            output_file = tempfile.NamedTemporaryFile(delete=False)

            text = end.decode()
            input_file.write(text)
            input_file.close()

            if 'lt-proc' == command[0]:
                lt_proc_command, dictionary_path = command[:-1], command[-1]
                lttoolbox.LtLocale.tryToSetLocale()
                fst = lttoolbox.FST(dictionary_path)
                if not fst.valid():
                    raise ValueError('FST Invalid')
                fst.lt_proc(lt_proc_command, input_file.name, output_file.name)
            elif 'lrx-proc' == command[0]:
                dictionary_path = command[-1]
                lextools.LtLocale.tryToSetLocale()
                lrx = lextools.LRXProc(dictionary_path)
                lrx_proc_command = command[:-1]
                lrx.lrx_proc(len(lrx_proc_command), lrx_proc_command, input_file.name, output_file.name)
            elif 'apertium-transfer' == command[0]:
                transfer = apertium_core.ApertiumTransfer(command[-2], command[-1])
                transfer_command = command[:-2]
                transfer.transfer_text(len(transfer_command), transfer_command, input_file.name, output_file.name)
            elif 'apertium-interchunk' == command[0]:
                interchunk = apertium_core.ApertiumInterchunk(command[-2], command[-1])
                interchunk_command = command[:-2]
                interchunk.interchunk_text(len(interchunk_command), interchunk_command, input_file.name, output_file.name)
            elif 'apertium-postchunk' == command[0]:
                postchunk = apertium_core.ApertiumPostchunk(command[-2], command[-1])
                postchunk_command = command[:-2]
                postchunk.postchunk_text(len(postchunk_command), postchunk_command, input_file.name, output_file.name)
            elif 'apertium-pretransfer' == command[0]:
                command = ['apertium-pretransfer', '']
                apertium_core.pretransfer(len(command), command, input_file.name, output_file.name)
            elif 'apertium-tagger' == command[0]:
                command += [input_file.name, output_file.name]
                apertium_core.ApertiumTagger(len(command), command)
            elif 'cg-proc' == command[0]:
                dictionary_path = command[-1]
                cg = constraint_grammar.CGProc(dictionary_path)
                cg_proc_command = command[:-1]
                cg.cg_proc(len(cg_proc_command), cg_proc_command, input_file.name, output_file.name)
            else:
                used_wrapper = False

            if used_wrapper:
                output_file.seek(0)
                end = output_file.read()
            output_file.close()

            os.remove(input_file.name)
            os.remove(output_file.name)
        if not wrappers_available or not used_wrapper:
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
