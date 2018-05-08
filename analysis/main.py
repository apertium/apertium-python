import re

import utils
from modesearch import search_path
from translation import execute

class Analyzer:
    '''
    Abstraction of morphological analyzer
    '''
    
    def __init__(self, pair_path):
        '''
        initialization tasks like setting the pair path,
        searching for the analyzers and installs modes
        '''
        
        self.pair_path = pair_path
        self.analyzers = {}
        
        modes = search_path(self.pair_path)
        
        for dirpath, modename, lang_pair in modes['analyzer']:
            self.analyzers[lang_pair] = (dirpath, modename)

    def postproc_text(self, in_text, result):
        '''
        postprocesses the input
        '''

        lexical_units = utils.remove_dot_from_deformat(in_text, re.findall(r'\^([^\$]*)\$([^\^]*)', result))
        return [(lu[0], lu[0].split('/')[0] + lu[1])
                for lu
                in lexical_units]


    def analyze(self, text, lang):
        '''
        runs apertium to analyze the input
        '''

        in_text = text
        in_mode = utils.to_alpha3_code(lang)

        if in_mode in self.analyzers:
            path, mode = self.analyzers[in_mode]
            formatting = 'txt'
            commands = [['apertium', '-d', path, '-f', formatting, mode]]
            result = execute(in_text, commands)
            return self.postproc_text(in_text, result)
        
        else:
            print("explanation='That mode is not installed")



        
