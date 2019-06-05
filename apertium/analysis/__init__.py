import os
import tempfile
from streamparser import parse, LexicalUnit  # noqa: F401
import analysis

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
        self.analyzer_path = []  # type: List[str]
        self.lang = to_alpha3_code(lang)  # type: str
        if self.lang not in apertium.analyzers:
            raise apertium.ModeNotInstalled(self.lang)
        else:
            self.path, self.mode = apertium.analyzers[self.lang]

    def _get_path(self):  # type: (Analyzer) -> List[str]
        """
        Read mode file for automorf.bin path

        Returns:
            List[str]
        """
        if self.lang not in self.analyzer_cmds:
            mode_path, mode = apertium.analyzers[self.lang]
            mode_path = os.path.join(mode_path, "modes", "{}.mode".format(mode))
            self.analyzer_cmds[self.lang] = parse_mode_file(mode_path)
            self.analyzer_path = [command[-1] for command in self.analyzer_cmds[self.lang]]
        return self.analyzer_path

    @staticmethod
    def _lt_proc(input_text, automorf_path):  # type: (str, str) -> str
        """
        Reads formatted text from apertium-des and returns its analysis

        Args:
            input_text (str)
            automorf_path (str)

        Returns:
            str
        """
        with tempfile.NamedTemporaryFile("w") as input_file, tempfile.NamedTemporaryFile("r") as output_file:
            input_file.write(input_text)
            input_file.flush()
            x = analysis.FST()
            if not x.valid():
                raise ValueError("FST Invalid")
            x.analyze(automorf_path, input_file.name, output_file.name)
            return output_file.read()

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
        apertium_des = execute(in_text, [['apertium-des{}'.format(formatting), '-n']])
        result = self._lt_proc(apertium_des, self._get_path()[0])
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
