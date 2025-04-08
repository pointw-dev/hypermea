#!/usr/bin/env python

"""
    Use this file to desk-check functions defined in your service.
    For example, when fussing with `starting_environment()` I found
    it easier just to iterate from here.
"""

import os
import json
import sys
from pathlib import Path

# Add src/service to sys.path
service_dir = Path(__file__).resolve().parents[1] / "service"
sys.path.insert(0, str(service_dir))

from hypermea.core.settings import starting_environment


def main():
    print(json.dumps(starting_environment(), indent=4))


if __name__ == '__main__':
    main()
