import os
from typing import Dict, List

from streamparser import LexicalUnit, parse

import apertium
from apertium.utils import execute, parse_mode_file, to_alpha3_code


class Analyzer:
    """
    Attributes:
        analyzer_cmds (Dict[str, List[List[str]]])
        lang (str)
    """

    def __init__(self, lang: str) -> None:
        """
        Args:
            lang (str)
        """
        self.analyzer_cmds: Dict[str, List[List[str]]] = {}
        self.lang: str = to_alpha3_code(lang)
        if self.lang not in apertium.analyzers:
            raise apertium.ModeNotInstalled(self.lang)
        else:
            self.path, self.mode = apertium.analyzers[self.lang]

    def _get_commands(self) -> List[List[str]]:
        """
        Returns:
            List[List[str]]
        """
        if self.lang not in self.analyzer_cmds:
            mode_path, mode = apertium.analyzers[self.lang]
            abs_mode_path = os.path.join(mode_path, 'modes', '{}.mode'.format(mode))
            self.analyzer_cmds[self.lang] = parse_mode_file(abs_mode_path)

        return self.analyzer_cmds[self.lang]

    @staticmethod
    def _postproc_text(result: str) -> List[LexicalUnit]:
        """
        Postprocesses the input

        Args:
            result (str)

        Returns:
            List[LexicalUnit]
        """
        lexical_units = list(parse(result))
        return lexical_units

    def analyze(self, in_text: str, formatting: str = 'txt') -> List[LexicalUnit]:
        """
        Runs apertium to analyze the input

        Args:
            in_text (str)
            formatting (str)

        Returns:
            List[LexicalUnit]
        """
        self._get_commands()
        deformatter = ['apertium-des{}'.format(formatting), '-n']
        if deformatter not in self.analyzer_cmds[self.lang]:
            self.analyzer_cmds[self.lang].insert(0, deformatter)
        result = execute(in_text, self.analyzer_cmds[self.lang])
        return self._postproc_text(result)


def analyze(lang: str, in_text: str, formatting: str = 'txt') -> List[LexicalUnit]:
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
