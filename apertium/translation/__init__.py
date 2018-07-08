import re
from subprocess import Popen, PIPE, CalledProcessError

if False:
    from typing import List, Dict, Tuple, Union, Optional, NamedTuple, Any  # noqa: F401

import apertium  # noqa: F401
from apertium.utils import to_alpha3_code, execute, parse_mode_file  # noqa: F401


class Translator:
    def __init__(self, l1, l2):  # type: (Translator, str, str) -> None
        """
        initializes the Translator object
        """
        self.translation_cmds = {}  # type: Dict[Tuple[str, str], List[List[str]]]
        self.l1 = l1
        self.l2 = l2

    def __repr__(self):  # type: (Translator) -> str
        """
        returns the representation of this Translator class object
        """
        return 'Translator(pair=%s-%s)' % (self.l1, self.l2)

    def __str__(self):  # type: (Translator) -> str
        """
        returns the printable str representation of the Translator object
        """
        return '<Translator: %s>' % apertium.pairs['%s-%s' % (self.l1, self.l2)].split('/')[-1]

    def _get_commands(self, l1, l2):  # type: (Translator, str, str) -> List[List[str]]
        """
        returns the commands to run for the analysis
        """
        if (l1, l2) not in self.translation_cmds:
            mode_path = apertium.pairs['%s-%s' % (l1, l2)]
            self.translation_cmds[(l1, l2)] = parse_mode_file(mode_path)
        return self.translation_cmds[(l1, l2)]

    def _get_format(self, format, deformat, reformat):
        # type: (Translator, Optional[str], Optional[str], Optional[str]) -> Tuple[Optional[str], Optional[str]]
        """
        returns the appropriate deformat and reformat arguments
        """
        if format:
            deformat = 'apertium-des' + str(format)
            reformat = 'apertium-re' + str(format)
        else:
            if 'apertium-des' not in str(deformat):
                deformat = 'apertium-des' + str(deformat)
            if 'apertium-re' not in str(reformat):
                reformat = 'apertium-re' + str(reformat)

        return deformat, reformat

    def _check_ret_code(self, proc):  # type: (Translator, Popen) -> None
        """
        validates if the process was executed succesfully
        """
        if proc.returncode != 0:
            raise CalledProcessError()  # type: ignore

    def _validate_formatters(self, deformat, reformat):
        # type: (Translator, Optional[str], Optional[str]) -> Tuple[Union[str, object], Union[str, object]]
        """
        returns validated formatting arguments
        """
        def valid1(elt, lst):  # type: (Optional[str], List[object]) -> Union[str, object]
            if elt in lst:
                return elt
            else:
                return lst[0]
        # First is fallback:
        deformatters = [
            'apertium-deshtml',
            'apertium-destxt',
            'apertium-desrtf',
            False,
        ]
        reformatters = [
            'apertium-rehtml-noent',
            'apertium-rehtml',
            'apertium-retxt',
            'apertium-rertf',
            False,
        ]
        return valid1(deformat, deformatters), valid1(reformat, reformatters)

    def _get_deformat(self, deformat, text):  # type: (Translator, str, str) -> str
        if deformat:
            proc_deformat = Popen(deformat, stdin=PIPE, stdout=PIPE)
            proc_deformat.stdin.write(bytes(text, 'utf-8'))
            deformatted = proc_deformat.communicate()[0]
            deformatted = deformatted.decode()
            self._check_ret_code(proc_deformat)
        else:
            deformatted = bytes(text, 'utf-8')
        res = str(deformatted)
        return res

    def _get_reformat(self, reformat, text):  # type: (Translator, str, str) -> Any
        if reformat:
            proc_reformat = Popen(reformat, stdin=PIPE, stdout=PIPE)
            proc_reformat.stdin.write(bytes(text, 'utf-8'))
            result = proc_reformat.communicate()[0]
            self._check_ret_code(proc_reformat)
        else:
            result = re.sub(rb'\0$', b'', text)  # type: ignore
        return result

    def translate(self, text, mark_unknown=False, format=None, deformat='txt', reformat='txt'):
        # type: (Translator, str, bool, Optional[str], str, str) -> Any
        """
        returns the translated text
        """
        l1, l2 = map(to_alpha3_code, [self.l1, self.l2])
        if '%s-%s' % (l1, l2) in apertium.pairs:
            pair = map(to_alpha3_code, [self.l1, self.l2])
        else:
            raise apertium.ModeNotInstalled()

        if pair is not None:
            l1, l2 = pair
            cmds = list(self._get_commands(l1, l2))
            unsafe_deformat, unsafe_reformat = self._get_format(format, deformat, reformat)
            deformater, reformater = self._validate_formatters(unsafe_deformat, unsafe_reformat)
            deformatted = self._get_deformat(str(deformater), text)
            output = execute(deformatted, cmds)
            result = self._get_reformat(str(reformater), output).strip()
            return result.decode()


def translate(l1, l2, text, mark_unknown=False, format=None, deformat='txt', reformat='txt'):
    # type: (str, str, str, bool, Optional[str], str, str) -> str
    """
    directly returns the translation from apertium
    """
    translator = apertium.Translator(l1, l2)
    return translator.translate(text, mark_unknown, format, deformat, reformat)  # type: ignore
