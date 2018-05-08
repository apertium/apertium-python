# -*- coding: utf-8 -*-

#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this file. If not, see <http://www.gnu.org/licenses/>.
#
#   Copyright © 2013-2018 The University of Tromsø &
#                         the Norwegian Sámi Parliament
#   http://giellatekno.uit.no & http://divvun.no
#
"""Classes and functions to do handle apertium modes.xml files."""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

from corpustools import util


class Pipeline(object):
    """Make a pipeline out of modes.xml file.
        
        Attributes:
        mode (lxml.Element): a mode element from a modes.xml file
        relative_path (str): relative path to the filenames given in the
        modes.xml file.
        """
    
    def __init__(self, mode, relative_path):
        """Initialise the Pipeline class.
            
            Arguments:
            mode (lxml.Element): a mode element from a modes.xml file.
            relative_path (str): relative path to the filenames given in the
            modes.xml file.
            """
        self.mode = mode
        self.relative_path = relative_path
    
    @staticmethod
    def raise_unless_exists(filenames):
        """Raise an ArgumentError if filename does not exist.
            
            Arguments:
            filenames (list of str): list of filenames harvested from the
            mode element.
            
            Raises:
            util.ArgumentError if a filename does not exist.
            """
        for filename in filenames:
            if not os.path.exists(filename):
                raise (util.ArgumentError(
                                          'ERROR: {} does not exist'.format(filename)))

def sanity_check(self):
    """Check that programs and files found in a program element exist."""
        util.sanity_check(
                          [program.get('name') for program in self.mode.iter('program')])
                          self.raise_unless_exists([
                                                    os.path.join(self.relative_path, file_elem.get('name'))
                                                    for file_elem in self.mode.iter('file')
                                                    ])

def run_external_command(self, command, instring):
    """Run the command with input using subprocess.
        
        Arguments:
        command (list of str): a subprocess compatible command.
        instring (bytes): the input to the command.
        
        Returns:
        bytes: the output of the command
        """
            runner = util.ExternalCommandRunner()
            runner.run(command, to_stdin=instring)
            self.check_error(command, runner.stderr)
            
                return runner.stdout

@staticmethod
    def check_error(command, error):
        """Print errors."""
        if error:
            print(
                  u'{} failed:\n{}'.format(u' '.join(command),
                                           error.decode('utf8')),
                  file=sys.stderr)

def tag2commandpart(self, element):
    """Turn program elements to a command part.
        
        Arguments:
        element (lxml.Element): a program subelement
        
        Returns:
        str: a program, a program option or a path to a file
        """
            if element.tag == 'file':
            return os.path.join(self.relative_path, element.get('name'))
                else:
                    return element.get('name')

def program2command(self, program):
    """Turn a program element to a subprocess compatible command.
        
        Arguments:
        program (str): a program element
        
        Returns:
        list of str: a subprocess compatible command
        """
            return [self.tag2commandpart(element) for element in program.iter()]

        @property
            def commands(self):
        """Make a list of subprocess compatible commands.
            
            Returns:
            list of list: a list of subprocess compatible commands.
            """
return [
        self.program2command(program)
        for program in self.mode.iter('program')
        ]

    def run(self, instring):
        """Run the pipeline using input.
            
            Arguments:
            instring (bytes): utf-8 encoded input to the pipeline
            
            Returns:
            str: output of the pipeline
            """
        for command in self.commands:
            instring = self.run_external_command(command, instring)
        
        return instring.decode('utf8')
