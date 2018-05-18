from streamparser import parse

import utils as utils
from modesearch import search_path
from translation import execute


class Analyzer:
    """
    Abstraction of morphological analyzer
    """
    def __init__(self):
        """
        initialization tasks like setting the pair path,
        searching for the analyzers and installs modes
        """
        self.pair_paths = ['/usr/share/apertium', '/usr/local/share/apertium']
        self.analyzers = {}
        for pair_path in self.pair_paths:
            self.update_modes(pair_path)

    def update_modes(self, pair_path):
        modes = search_path(pair_path)
        if len(modes['analyzer']) is not 0:
                for dirpath, modename, lang_pair in modes['analyzer']:
                    self.analyzers[lang_pair] = (dirpath, modename)

    def append_pair_path(self, pair_path):
        self.pair_paths.append(pair_path)
        self.update_modes(pair_path)

    def postproc_text(self, in_text, result):
        """
        postprocesses the input
        """
        lexical_units = parse(result)
        return list(lexical_units)[0]

    def analyze(self, text, lang):
        """
        runs apertium to analyze the input
        """
        in_text = text
        in_mode = utils.to_alpha3_code(lang)

        if in_mode in self.analyzers:
            path, mode = self.analyzers[in_mode]
            formatting = 'txt'
            commands = [['apertium', '-d', path, '-f', formatting, mode]]
            result = execute(in_text, commands)
            return self.postproc_text(in_text, result)

        else:
            return None
