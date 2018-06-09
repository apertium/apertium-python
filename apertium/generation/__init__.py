from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Tuple, Dict  # noqa: F401

pipeline_cmds = {}  # type: Dict[str, List[List[str]]]


def get_pipe_cmds(lang):  # type: (str) -> List[List[str]]
    if lang not in pipeline_cmds:
        mode_path, mode = apertium.generators[lang]
        pipeline_cmds[lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
    return pipeline_cmds[lang]


def generate(lang, in_text, formatting='none'):  # type: (str, str, str) -> Union[str, List[str]]
    lang = to_alpha3_code(lang)

    if lang in apertium.generators:
        commands = list(get_pipe_cmds(lang))
        result = execute(in_text, commands)
        return result
    else:
        raise apertium.ModeNotInstalled(lang)
