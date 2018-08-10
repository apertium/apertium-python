from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Tuple, Dict  # noqa: F401


class Generator:
    """An Generator object containing it's generation mode and langugage. 
    The language is taken as input and then all the generators corresponding to the particular language
    that are installed are looked up and used.

    Args:
        generator_cmds (Dict[str, List[List[str]]]): stores the commands for various generators to run succesfully. 
        lang (str): Language of the text which is morphologically generated. 
    """
    def __init__(self, lang):  # type: (Generator, str) -> None
        self.generator_cmds = {}  # type: Dict[str, List[List[str]]]
        self.lang = lang  # type: str

    def _get_commands(self):  # type: (Generator) -> List[List[str]]
        """Returns the commands to run for the generation 

        Args:
            Object of class Generator 

        Yeilds:
            A List[List[str]] having the commands that need to be run for the particular mode execution. 
        """
        if self.lang not in self.generator_cmds:
            mode_path, mode = apertium.generators[self.lang]
            self.generator_cmds[self.lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.generator_cmds[self.lang]

    def generate(self, in_text, formatting='none'):  # type: (Generator, str, str) -> Union[str, List[str]]
        """Generates the word form for the analysis provided 

        Args:
            in_text (str): The analysis from which a wordform has to be generated 
            formatting (str): The output format of the generated wordform 

        Yields:
            List[str] of the output of correct wordform/wordforms of the input. 
        """
        self.lang = to_alpha3_code(self.lang)

        if self.lang in apertium.generators:
            commands = list(self._get_commands())
            result = execute(in_text, commands)
            return result.rstrip('\x00')
        else:
            raise apertium.ModeNotInstalled(self.lang)


def generate(lang, in_text, formatting='none'):    # type: (str, str, str) -> Union[str, List[str]]
    """Directly returns the generated output from apertium 
    """
    generator = Generator(lang)
    return generator.generate(in_text, formatting)
