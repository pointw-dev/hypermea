#!/usr/bin/env python
"""Adds custom validation module to the API project.

This also adds two new validation rules
- unique_to_parent
    - the field must be unique amongst other resources with the same parent_ref, but can
      be repeated within other parents
- unique_ignorecase
    - prevents the same value being considered unique when the only difference is case
      e.g. 'station #1' will be considered the same as 'Station #1', the rule will
      prevent whichever is second from being inserted.

Usage:
    add-validation

Examples:
    add-validation

License:
    MIT License

    Copyright (c) 2021 Michael Ottoson

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import os
from hypermea.code_gen import ValidationInserter
import hypermea


def wire_up_service():
    ValidationInserter().transform('hypermea_service.py')


def add(silent=False):
    try:
        starting_folder, settings = hypermea.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1, silent)

    if os.path.exists('./validation'):
        return hypermea.escape('validation has already been added', 301, silent)

    hypermea.copy_skel(settings['project_name'], 'validation', silent=silent)
    hypermea.install_packages(['isodate'], 'add-validation')
    wire_up_service()

    hypermea.jump_back_to(starting_folder)
    return hypermea.escape('validation module added', 0, silent)
