from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Dict  # noqa: F401


class Analyzer:
    def __init__(self, lang):  # type: (Analyzer, str) -> None
        """
        initializes the Analyzer object
        """
        self.analyzer_cmds = {}  # type: Dict[str, List[List[str]]]
        self.lang = to_alpha3_code(lang)  # type: str
        if self.lang not in apertium.analyzers:
            raise apertium.ModeNotInstalled(self.lang)
        else:
            self.path, self.mode = apertium.analyzers[self.lang]

    def __repr__(self):  # type: (Analyzer) -> str
        """
        returns the representation of this Analyzer class object
        """
        return 'Analyzer(lang=%s)' % self.lang

    def __str__(self):  # type: (Analyzer) -> str
        """
        returns the printable str representation of the object
        """
        return '<Analyzer: %s>' % self.mode

    def _get_commands(self):  # type: (Analyzer) -> List[List[str]]
        """
        returns the commands to run for the analysis
        """
        if self.lang not in self.analyzer_cmds:
            mode_path, mode = apertium.analyzers[self.lang]
            self.analyzer_cmds[self.lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.analyzer_cmds[self.lang]

    def _postproc_text(self, result):  # type: (Analyzer, str) -> List[LexicalUnit]
        """
        postprocesses the input
        """
        lexical_units = list(parse(result))
        return lexical_units

    def analyze(self, in_text, formatting='txt'):  # type: (Analyzer, str, str) -> List[LexicalUnit]
        """
        runs apertium to analyze the input
        """
        commands = [['apertium', '-d', self.path, '-f', formatting, self.mode]]
        result = execute(in_text, commands)
        return self._postproc_text(result)


def analyze(lang, in_text, formatting='txt'):  # type: (str, str, str) -> List[LexicalUnit]
    """
    directly returns the analysis from apertium
    """
    analyzer = Analyzer(lang)
    return analyzer.analyze(in_text, formatting)
