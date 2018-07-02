from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Tuple, Dict  # noqa: F401


class Generator:
    def __init__(self, lang):  # type: (Generator, str) -> None
        self.generator_cmds = {}  # type: Dict[str, List[List[str]]]
        self.lang = to_alpha3_code(lang)  # type: str
        if self.lang in apertium.generators:
            self.path, self.mode = apertium.generators[self.lang] 
            self.commands = list(self._get_commands())
        else:
            raise apertium.ModeNotInstalled(self.lang)

    def __repr__(self):  # type: (Analyzer) -> str
        return 'Generator(lang=%s)' % self.lang

    def __str__(self):  # type: (Analyzer) -> str

        return '<Generator: %s>' % self.mode

    def _get_commands(self):  # type: (Generator) -> List[List[str]]
        if self.lang not in self.generator_cmds:
            mode_path, mode = apertium.generators[self.lang]
            self.generator_cmds[self.lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.generator_cmds[self.lang]

    def generate(self, in_text, formatting='none'):  # type: (Generator, str, str) -> Union[str, List[str]]
        result = execute(in_text, self.commands)
        return result.rstrip('\x00')


def generate(lang, in_text, formatting='none'):    # type: (str, str, str) -> Union[str, List[str]]
    generator = Generator(lang)
    return generator.generate(in_text, formatting)
