#!/usr/bin/env python
"""Adds authorization module to the API project.

Usage:
    add-auth

Examples:
    add-auth

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
from hypermea.code_gen import AuthorizationInserter
import hypermea

# TODO: script getting default values (e.g. client keys)
# TODO: provide non Auth0


def wire_up_service():
    AuthorizationInserter().transform('hypermea_service.py', )


def add(silent=False):
    try:
        settings = hypermea.jump_to_api_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1, silent)

    if os.path.exists('./auth'):
        hypermea.escape('auth has already been added', 201, silent)

    hypermea.copy_skel(settings['project_name'], 'auth', silent=silent)
    hypermea.install_packages(['eve-negotiable-auth', 'PyJWT', 'cryptography', 'requests'], 'add-auth')
    # eve_negotiable_auth also installs authparser and pyparsing    
    # cryptography also installs cffi, pycparser
    # requests also installs certifi, chardet, idna, urllib3
    wire_up_service()
    
    return hypermea.escape('auth modules added', 0, silent)
