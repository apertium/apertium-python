import os
from typing import Dict, List

from streamparser import LexicalUnit, parse

import apertium
from apertium.utils import execute_pipeline, parse_mode_file, to_alpha3_code


class Tagger:
    """
    Attributes:
        tagger_cmds (Dict[str, List[List[str]]])
        lang (str)
    """

    def __init__(self, lang: str) -> None:
        """
        Args:
            lang (str)
        """
        self.tagger_cmds = {}  # type: Dict[str, List[List[str]]]
        self.lang = to_alpha3_code(lang)  # type: str
        if self.lang not in apertium.taggers:
            raise apertium.ModeNotInstalled(self.lang)
        else:
            self.path, self.mode = apertium.taggers[self.lang]

    def _get_commands(self) -> List[List[str]]:
        """
        Returns:
            List[List[str]]
        """
        if self.lang not in self.tagger_cmds:
            mode_path, mode = apertium.taggers[self.lang]
            abs_mode_path = os.path.join(mode_path, 'modes', '{}.mode'.format(mode))
            self.tagger_cmds[self.lang] = parse_mode_file(abs_mode_path)

        return self.tagger_cmds[self.lang]

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

    def tag(self, in_text: str, formatting: str = 'txt') -> List[LexicalUnit]:
        """
        Runs apertium to tagger the input

        Args:
            in_text (str)
            formatting (str)

        Returns:
            List[LexicalUnit]
        """
        self._get_commands()
        deformatter = ['apertium-des{}'.format(formatting), '-n']
        if deformatter not in self.tagger_cmds[self.lang]:
            self.tagger_cmds[self.lang].insert(0, deformatter)
        result = execute_pipeline(in_text, self.tagger_cmds[self.lang])
        return self._postproc_text(result)


def tag(lang: str, in_text: str, formatting: str = 'txt') -> List[LexicalUnit]:
    """
    Args:
        lang (str)
        in_text (str)
        formatting (str)

    Returns:
        List[LexicalUnit]
    """
    tagger = Tagger(lang)
    return tagger.tag(in_text, formatting)
