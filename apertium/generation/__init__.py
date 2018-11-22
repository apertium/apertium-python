import apertium  # type: ignore
from apertium.utils import to_alpha3_code, execute, parse_mode_file  # type: ignore

if False:
    from typing import List, Union, Tuple, Dict  # noqa: F401


class Generator:
    """
    Attributes:
        generation_cmds (Dict[str, List[List[str]]])
        lang (str)
    """

    def __init__(self, lang):
        # type: (Generator, str) -> None
        """
        Args:
            lang (str)
        """
        self.generator_cmds = {}  # type: Dict[str, List[List[str]]]
        self.lang = lang  # type: str

    def _get_commands(self):
        # type: (Generator) -> List[List[str]]
        """
        Returns:
            List[List[str]]
        """
        if self.lang not in self.generator_cmds:
            mode_path, mode = apertium.generators[self.lang]
            self.generator_cmds[self.lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.generator_cmds[self.lang]

    def generate(self, in_text, formatting='none'):
        # type: (Generator, str, str) -> Union[str, List[str]]
        """
        Args:
            in_text (str)
            formatting (str)

        Returns:
            Union[str, List[str]]
        """
        self.lang = to_alpha3_code(self.lang)

        if self.lang in apertium.generators:
            commands = list(self._get_commands())
            result = execute(in_text, commands)
            return result.rstrip('\x00')
        else:
            raise apertium.ModeNotInstalled(self.lang)


def generate(lang, in_text, formatting='none'):
    # type: (str, str, str) -> Union[str, List[str]]
    """
    Args:
        lang (str)
        in_text (str)
        formatting (str)

    Returns:
        Union[str, List[str]]
    """
    generator = Generator(lang)
    return generator.generate(in_text, formatting)
