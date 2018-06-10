from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Tuple, Dict  # noqa: F401

class Generator:

    def __init__(self):
        self.generator_cmds = {}  # type: Dict[str, List[List[str]]]


    def _get_commands(self, lang):  # type: (str) -> List[List[str]]
        if lang not in self.generator_cmds:
            mode_path, mode = apertium.generators[lang]
            self.generator_cmds[lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.generator_cmds[lang]


    def generate(lang, in_text, formatting='none'):  # type: (str, str, str) -> Union[str, List[str]]
        lang = to_alpha3_code(lang)

        if lang in apertium.generators:
            commands = list(self._get_commands(lang))
            result = execute(in_text, commands)
            return result
        else:
            raise apertium.ModeNotInstalled(lang)
