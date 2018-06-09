from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Dict  # noqa: F401

pipeline_cmds = {}  # type: Dict[str, List[List[str]]]


def get_pipe_cmds(lang):  # type: (str) -> List[List[str]]
    if lang not in pipeline_cmds:
        mode_path, mode = apertium.analyzers[lang]
        pipeline_cmds[lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
    return pipeline_cmds[lang]


def postproc_text(result):  # type: (str) -> List[LexicalUnit]
    """
    postprocesses the input
    """
    lexical_units = list(parse(result))
    return lexical_units


def analyze(lang, in_text, formatting='txt'):  # type: (str, str, str) -> List[LexicalUnit]
    """
    runs apertium to analyze the input
    """
    lang = to_alpha3_code(lang)

    if lang in apertium.analyzers:
        in_text = in_text
        commands = list(get_pipe_cmds(lang))
        result = execute(in_text, commands)
        return postproc_text(result)
    else:
        raise apertium.ModeNotInstalled(lang)
