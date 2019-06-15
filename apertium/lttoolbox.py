import tempfile
from typing import ByteString, List  # noqa: F401

import lttoolbox


class LtProc:
    """
    Attributes:
        command (List)
        path (str)
        input_text (str)
        output_text (str)
    """

    def __init__(self, command: List, input_text: str) -> None:
        """
        Args:
            command (List)
            input_text (str)
        """
        self.command = command
        self.path = command[-1]
        self.input_text = input_text
        self.output_text = ''

    def execute(self) -> ByteString:
        """
        Executes the required method, depending upon the argument for lt-proc

        Args:
            self (LtProc)

        Returns:
            (ByteString)
        """
        with tempfile.NamedTemporaryFile('w') as input_file, tempfile.NamedTemporaryFile('r') as output_file:
            input_file.write(self.input_text)
            input_file.flush()
            lttoolbox.LtLocale.tryToSetLocale()
            fst = lttoolbox.FST()
            if not fst.valid():
                raise ValueError('FST Invalid')
            if '-w' in self.command:
                fst.setDictionaryCaseMode(True)
                fst.analyze(self.path, input_file.name, output_file.name)
            elif '-g' in self.command:
                fst.generate(self.path, input_file.name, output_file.name)

            self.output_text = output_file.read()
            return self.output_text.encode()
