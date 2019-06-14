import platform
import tempfile
from typing import ByteString  # noqa: F401

import lttoolbox


class LtProc:
    """
    Attributes:
        arg_index (int)
        path (str)
        input_text (str)
        output_text (str)
    """

    def __init__(self, input_text: str, arg_index: str, path: str) -> None:
        """
        Args:
            input_text (str)
            arg_index (int)
            path (str)
        """
        self.arg_index = arg_index
        self.path = path
        self.input_text = input_text
        self.output_text = ''

    def analyze(self) -> None:
        """
        Reads formatted text from apertium-des and returns its analysed text

        Args:
            self (LtProc)
        Returns:
            None
        """
        with tempfile.NamedTemporaryFile('w') as input_file, tempfile.NamedTemporaryFile('r') as output_file:
            input_file.write(self.input_text)
            input_file.flush()
            fst = lttoolbox.FST()
            if not fst.valid():
                raise ValueError('FST Invalid')
            fst.analyze(self.path, input_file.name, output_file.name)
            self.output_text = output_file.read()

    def execute(self) -> ByteString:
        """
        Executes the required method, depending upon the argument for lt-proc

        Args:
            self (LtProc)

        Returns:
            (ByteString)
        """
        if self.arg_index == '-w':
            self.analyze()
            return self.output_text.encode()
