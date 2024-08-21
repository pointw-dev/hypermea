# https://chatgpt.com/share/c2e7ee0e-fd99-48c7-a44b-76d388383377

import os
import subprocess
import sys


class TerminalHarness():
    def __init__(self):
        self.result = None
        self.output = ''


    def run(self, command):
        self.result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return self

    @property
    def console(self):
        self.output = self.result.stdout
        return self

    def displays(self, expected_output):
        assert expected_output in self.output, f"Expected '{expected_output}' to be in console output"
        return self

    def file(self, filename):
        self.filename = filename
        return self

    def contains(self, expected_content):
        with open(self.filename, 'r') as file:
            content = file.read()
        assert expected_content in content, f"Expected '{expected_content}' to be in file content"
        return self

    def does_not_contain(self, unexpected_content):
        with open(self.filename, 'r') as file:
            content = file.read()
        assert unexpected_content not in content, f"Did not expect '{unexpected_content}' to be in file content"
        return self

    def exists(self):
        assert os.path.isfile(self.filename), f"Expected file '{self.filename}' to exist"
        return self

    def does_not_exist(self):
        assert not os.path.isfile(self.filename), f"Expected file '{self.filename}' to not exist"
        return self
