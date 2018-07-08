from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Tuple, Dict  # noqa: F401


class Generator:
    def __init__(self, lang):  # type: (Generator, str) -> None
        """
        initializes the Generator object
        """
        self.generator_cmds = {}  # type: Dict[str, List[List[str]]]
        self.lang = lang  # type: str

    def _get_commands(self):  # type: (Generator) -> List[List[str]]
        """
        returns the commands to run for the analysis
        """
        if self.lang not in self.generator_cmds:
            mode_path, mode = apertium.generators[self.lang]
            self.generator_cmds[self.lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.generator_cmds[self.lang]

    def generate(self, in_text, formatting='none'):  # type: (Generator, str, str) -> Union[str, List[str]]
        """
        returns the generated output from the morphological analysis provided
        """
        self.lang = to_alpha3_code(self.lang)

        if self.lang in apertium.generators:
            commands = list(self._get_commands())
            result = execute(in_text, commands)
            return result.rstrip('\x00')
        else:
            raise apertium.ModeNotInstalled(self.lang)


def generate(lang, in_text, formatting='none'):    # type: (str, str, str) -> Union[str, List[str]]
    """
    directly returns the generated output from apertium
    """
    generator = Generator(lang)
    return generator.generate(in_text, formatting)
