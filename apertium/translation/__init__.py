from apertium.utils import to_alpha3_code, execute, parse_mode_file  # type: ignore
import apertium  # type: ignore
import re
from subprocess import Popen, PIPE, CalledProcessError


class Translator:
    """
    Attributes:
        translation_cmds (Dict[Tuple[str, str], List[List[str]]])
        l1 (str)
        l2 (str)
    """

    def __init__(self, l1, l2):
        # type: (Translator, str, str) -> None
        """
        Args:
            l1 (str)
            l2 (str)
        """
        self.translation_cmds = {}  # type: Dict[Tuple[str, str], List[List[str]]]
        self.l1 = l1
        self.l2 = l2

    def _get_commands(self, l1, l2):
        # type: (Translator, str, str) -> List[List[str]]
        """
        Args:
            l1 (str)
            l2 (str)

        Returns:
            List[List[str]]
        """
        if (l1, l2) not in self.translation_cmds:
            mode_path = apertium.pairs['%s-%s' % (l1, l2)]
            self.translation_cmds[(l1, l2)] = parse_mode_file(mode_path)
        return self.translation_cmds[(l1, l2)]

    def _get_format(self, format, deformat, reformat):
        # type: (Translator, Optional[str], Optional[str], Optional[str]) -> Tuple[Optional[str], Optional[str]]
        """
        Args:
            format (Optional[str])
            deformat (Optional[str])
            reformat (Optional[str])

        Returns:
            Tuple[Optional[str], Optional[str]]
        """
        if format:
            deformat = 'apertium-des' + format
            reformat = 'apertium-re' + format
        else:
            if 'apertium-des' not in deformat:  # type: ignore
                deformat = 'apertium-des' + deformat  # type: ignore
            if 'apertium-re' not in reformat:  # type: ignore
                reformat = 'apertium-re' + reformat  # type: ignore

        return deformat, reformat

    def _check_ret_code(self, proc):
        # type: (Translator, Popen) -> None
        """
        Args:
            proc (Popen)
        """
        if proc.returncode != 0:
            raise CalledProcessError()  # type: ignore

    def _validate_formatters(self, deformat, reformat):
        # type: (Translator, Optional[str], Optional[str]) -> Tuple[Union[str, object], Union[str, object]]
        """
        Args:
            deformat (Optional[str])
            reformat (Optional[str])

        Returns:
            Tuple[Union[str, object], Union[str, object]]
        """
        def valid1(elt, lst):
            # type: (Optional[str], List[object]) -> Union[str, object]
            """
            Args:
                elt (Optional[str])
                lst (List[object])

            Returns:
                Union[str, object]
            """
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

    def _get_deformat(self, deformat, text):
        # type: (Translator, str, str) -> str
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
            self._check_ret_code(proc_deformat)
        else:
            deformatted = bytes(text, 'utf-8')
        res = str(deformatted)
        return res

    def _get_reformat(self, reformat, text):
        # type: (Translator, str, str) -> str
        """
        Args:
            reformat (str)
            text (str)

        Returns:
            str
        """
        if reformat:
            proc_reformat = Popen(reformat, stdin=PIPE, stdout=PIPE)
            proc_reformat.stdin.write(bytes(text, 'utf-8'))
            result = proc_reformat.communicate()[0]
            self._check_ret_code(proc_reformat)
        else:
            result = re.sub(rb'\0$', b'', text)  # type: ignore
        return result  # type: ignore

    def translate(self, text, mark_unknown=False, format=None, deformat='txt', reformat='txt'):
        # type: (Translator, str, bool, Optional[str], str, str) -> str
        """
        Args:
            text (str)
            mark_unknown (bool)
            format (Optional[str])
            deformat (str)
            reformat (str)

        Returns:
            str
        """
        if '%s-%s' % tuple(map(to_alpha3_code, [self.l1, self.l2])) in apertium.pairs:  # type: ignore
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
            return result.decode()  # type: ignore


def translate(l1, l2, text, mark_unknown=False, format=None, deformat='txt', reformat='txt'):
    # type: (str, str, str, bool, Optional[str], str, str) -> str
    """
    Args:
        text (str)
        mark_unknown (bool)
        format (Optional[str])
        deformat (str)
        reformat (str)

    Returns:
        str
    """
    translator = apertium.Translator(l1, l2)
    return translator.translate(text, mark_unknown, format, deformat, reformat)
