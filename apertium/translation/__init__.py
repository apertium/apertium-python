import re
from subprocess import CalledProcessError, PIPE, Popen
from typing import Dict, List, Optional, Tuple, Union

import apertium  # noqa: E402
from apertium.utils import execute_pipeline, parse_mode_file, to_alpha3_code  # noqa: E402


class Translator:
    """
    Attributes:
        translation_cmds (Dict[Tuple[str, str], List[List[str]]])
        lang1 (str)
        lang2 (str)
    """

    def __init__(self, lang1: str, lang2: str) -> None:
        """
        Args:
            lang1 (str)
            lang2 (str)
        """
        self.translation_cmds: Dict[Tuple[str, str], List[List[str]]] = {}
        self.lang1 = lang1
        self.lang2 = lang2

    def _get_commands(self, lang1: str, lang2: str) -> List[List[str]]:
        """
        Args:
            lang1 (str)
            lang2 (str)

        Returns:
            List[List[str]]
        """
        if (lang1, lang2) not in self.translation_cmds:
            mode_path = apertium.pairs['%s-%s' % (lang1, lang2)]
            self.translation_cmds[(lang1, lang2)] = parse_mode_file(mode_path)
        return self.translation_cmds[(lang1, lang2)]

    def _get_format(self, formatting: Optional[str], deformat: Optional[str], reformat: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Args:
            formatting (Optional[str])
            deformat (Optional[str])
            reformat (Optional[str])

        Returns:
            Tuple[Optional[str], Optional[str]]
        """
        if formatting:
            deformat = 'apertium-des' + formatting
            reformat = 'apertium-re' + formatting
        else:
            if 'apertium-des' not in deformat:  # type: ignore
                deformat = 'apertium-des' + deformat  # type: ignore
            if 'apertium-re' not in reformat:  # type: ignore
                reformat = 'apertium-re' + reformat  # type: ignore

        return deformat, reformat

    def _check_ret_code(self, proc: Popen, cmd: str) -> None:
        """
        Args:
            proc (Popen)
            cmd (str)
        """
        if proc.returncode != 0:
            raise CalledProcessError(proc.returncode, cmd)

    def _validate_formatters(self, deformat: Optional[str], reformat: Optional[str]) -> Tuple[Union[str, bool], Union[str, bool]]:
        """
        Args:
            deformat (Optional[str])
            reformat (Optional[str])

        Returns:
            Tuple[Union[str, bool], Union[str, bool]]
        """
        def valid1(elt: Optional[str], lst: List[Union[str, bool]]) -> Union[str, bool]:
            """
            Args:
                elt (Optional[str])
                lst (List[Union[str, bool]])

            Returns:
                Union[str, bool]
            """
            if elt in lst:
                return elt
            else:
                return lst[0]

        # First is fallback:
        deformatters: List[Union[str, bool]] = [
            'apertium-deshtml',
            'apertium-destxt',
            'apertium-desrtf',
            False,
        ]
        reformatters: List[Union[str, bool]] = [
            'apertium-rehtml-noent',
            'apertium-rehtml',
            'apertium-retxt',
            'apertium-rertf',
            False,
        ]
        return valid1(deformat, deformatters), valid1(reformat, reformatters)

    def _get_deformat(self, deformat: str, text: str) -> str:
        """
        Args:
            deformat (str)
            text (str)

        Returns:
            str
        """
        if deformat:
            proc_deformat = Popen(deformat, stdin=PIPE, stdout=PIPE)
            proc_deformat.stdin.write(bytes(text, 'utf-8'))
            deformatted = proc_deformat.communicate()[0]
            deformatted = deformatted.decode()
            self._check_ret_code(proc_deformat, deformat)
        else:
            deformatted = bytes(text, 'utf-8')
        res = str(deformatted)
        return res

    def _get_reformat(self, reformat: str, text: str) -> bytes:
        """
        Args:
            reformat (str)
            text (str)

        Returns:
            str
        """
        result: bytes
        if reformat:
            proc_reformat = Popen(reformat, stdin=PIPE, stdout=PIPE)
            proc_reformat.stdin.write(bytes(text, 'utf-8'))
            result = proc_reformat.communicate()[0]
            self._check_ret_code(proc_reformat, reformat)
        else:
            result = re.sub(rb'\0$', b'', text)  # type: ignore
        return result

    def translate(self, text: str, mark_unknown: bool = False, formatting: Optional[str] = None, deformat: str = 'txt', reformat: str = 'txt') -> str:
        """
        Args:
            text (str)
            mark_unknown (bool)
            formatting (Optional[str])
            deformat (str)
            reformat (str)

        Returns:
            str
        """
        if '{}-{}'.format(*map(to_alpha3_code, [self.lang1, self.lang2])) in apertium.pairs:
            pair = map(to_alpha3_code, [self.lang1, self.lang2])
        else:
            raise apertium.ModeNotInstalled()

        if pair is not None:
            lang1, lang2 = pair
            cmds = list(self._get_commands(lang1, lang2))
            unsafe_deformat, unsafe_reformat = self._get_format(formatting, deformat, reformat)
            deformater, reformater = self._validate_formatters(unsafe_deformat, unsafe_reformat)
            deformatted = self._get_deformat(str(deformater), text)
            output = execute_pipeline(deformatted, cmds)
            result: bytes = self._get_reformat(str(reformater), output).strip()
            return result.decode()


def translate(lang1: str, lang2: str, text: str, mark_unknown: bool = False,
              formatting: Optional[str] = None, deformat: str = 'txt', reformat: str = 'txt') -> str:
    """
    Args:
        lang1: str
        lang2: str
        text (str)
        mark_unknown (bool)
        formatting (Optional[str])
        deformat (str)
        reformat (str)

    Returns:
        str
    """
    translator = Translator(lang1, lang2)
    return translator.translate(text, mark_unknown, formatting, deformat, reformat)
