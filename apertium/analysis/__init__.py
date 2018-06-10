from streamparser import parse, LexicalUnit  # noqa: F401

import apertium
from apertium.utils import to_alpha3_code, execute, parse_mode_file

if False:
    from typing import List, Union, Dict  # noqa: F401


class Analyzer:

    def __init__(self):
        self.analyzer_cmds = {}  # type: Dict[str, List[List[str]]]


    def _get_commands(self, lang):  # type: (str) -> List[List[str]]
        if lang not in self.analyzer_cmds:
            mode_path, mode = apertium.analyzers[lang]
            self.analyzer_cmds[lang] = parse_mode_file(mode_path+'/modes/'+mode+'.mode')
        return self.analyzer_cmds[lang]


    def _postproc_text(self, result):  # type: (str) -> List[LexicalUnit]
        """
        postprocesses the input
        """
        lexical_units = list(parse(result))
        return lexical_units


    def analyze(self, lang, in_text, formatting='txt'):  # type: (str, str, str) -> List[LexicalUnit]
        """
        runs apertium to analyze the input
        """
        lang = to_alpha3_code(lang)

        if lang in apertium.analyzers:
            commands = list(self._get_commands(lang))
            result = execute(in_text, commands)
            return self._postproc_text(result)
        else:
            raise apertium.ModeNotInstalled(lang)

