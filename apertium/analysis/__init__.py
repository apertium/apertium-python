from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Dict  # noqa: F401


class Analyzer:
    """
    Attributes:
        analyzer_cmds (Dict[str, List[List[str]]])
        lang (str)
    """

    def __init__(self, lang):  # type: (Analyzer, str) -> None
        """
        Args:
            lang (str)
        """
        self.analyzer_cmds = {}  # type: Dict[str, List[List[str]]]
        self.lang = to_alpha3_code(lang)  # type: str
        if self.lang not in apertium.analyzers:
            raise apertium.ModeNotInstalled(self.lang)
        else:
            self.path, self.mode = apertium.analyzers[self.lang]

    def _get_commands(self):  # type: (Analyzer) -> List[List[str]]
        """
        Returns:
            List[List[str]]
        """
        if self.lang not in self.analyzer_cmds:
            mode_path, mode = apertium.analyzers[self.lang]
            self.analyzer_cmds[self.lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.analyzer_cmds[self.lang]

    def _postproc_text(self, result):  # type: (Analyzer, str) -> List[LexicalUnit]
        """
        Postprocesses the input

        Args:
            result (str)

        Returns:
            List[LexicalUnit]
        """
        lexical_units = list(parse(result))
        return lexical_units

    def analyze(self, in_text, formatting='txt'):  # type: (Analyzer, str, str) -> List[LexicalUnit]
        """
        Runs apertium to analyze the input

        Args:
            in_text (str)
            formatting (str)

        Returns:
            List[LexicalUnit]
        """
        commands = [['apertium', '-d', self.path, '-f', formatting, self.mode]]
        result = execute(in_text, commands)
        return self._postproc_text(result)


def analyze(lang, in_text, formatting='txt'):  # type: (str, str, str) -> List[LexicalUnit]
    """
    Args:
        lang (str)
        in_text (str)
        formatting (str)

    Returns:
        List[LexicalUnit]
    """
    analyzer = Analyzer(lang)
    return analyzer.analyze(in_text, formatting)
