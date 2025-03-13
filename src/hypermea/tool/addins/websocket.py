#!/usr/bin/env python
"""Adds web socket functionality to API

Usage:
    add-websocket

Examples:
    add-websocket

License:
    MIT License

    Copyright (c) 2019-2025 Michael Ottoson (pointw.com)

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
import hypermea.tool


def modify_hypermea_service():
    with open('./hypermea_service.py', 'r') as f:
        lines = f.readlines()
        
    with open('./hypermea_service.py', 'w') as f:
        for line in lines:
            if 'from flask_cors import CORS' in line:
                f.write(line)
                f.write('from flask_socketio import SocketIO\n')
                f.write('import websocket\n')
            elif 'hooks.add_hooks(self._app)' in line:
                f.write(line)
                f.write("        self._socket = SocketIO(self._app, async_mode=None, path='/_ws/socket.io', cors_allowed_origins='*')\n")
                f.write("        websocket.initialize(self._app, self._socket)\n")
            elif 'self._app.run' in line:
                f.write("            self._socket.run(self._app, host='0.0.0.0', port=SETTINGS.get('HY_API_PORT'), allow_unsafe_werkzeug=True)\n")
            else:
                f.write(line)


def add(silent=False):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1, silent)

    if os.path.exists('./websocket'):
        hypermea.tool.jump_back_to(starting_folder)
        return hypermea.tool.escape('websocket has already been added', 501, silent)

    modify_hypermea_service()
    hypermea.tool.copy_skel(settings['project_name'], 'websocket', '.', silent=silent)
    hypermea.tool.install_packages(['Flask-SocketIO'], 'add-websocket')
    hypermea.tool.jump_back_to(starting_folder)
    return 0
