#!/usr/bin/env python

import os
import json
import platform
from eve import __version__ as eve_version
from cerberus import __version__ as cerberus_version
from hypermea.core import VERSION as hypermea_core_version
from werkzeug.utils import secure_filename

ALLURE_RESULTS_DIR = './allure-results'
ALLURE_REPORT_DIR = "./allure-report"


"""
executor.json

{
  "name": "Jenkins",
  "type": "jenkins",
  "url": "http://example.org",
  "buildOrder": 13,
  "buildName": "allure-report_deploy#13",
  "buildUrl": "http://example.org/build#13",
  "reportUrl": "http://example.org/build#13/AllureReport",
  "reportName": "Demo allure report"
}
"""

def create_executor_json():
    executor = {
        'name': 'run_tests_with_allure.py',
        'type': 'python script',
        'buildName': 'manually built'
    }
    with open(f'{ALLURE_RESULTS_DIR}/executor.json', 'w', encoding='utf8') as f:
        json.dump(executor, f, indent=4)


"""
environment.properties

os_platform = linux
os_release = 5.15.0-60-generic
os_version = #66-Ubuntu SMP Fri Jan 20 14:29:49 UTC 2023
python_version = Python 3.10.9
"""

def create_environment_properties():
    with open(f'{ALLURE_RESULTS_DIR}/environment.properties', 'w', encoding='utf8') as f:
        f.write(f'python = {platform.sys.version}\n')
        f.write(f'hypermea-core = {hypermea_core_version}\n')
        f.write(f'eve = {eve_version}\n')
        f.write(f'cerberus = {cerberus_version}\n')
        f.write(f'python = {platform.sys.version}\n')
        f.write(f'os_system = {platform.system()}\n')
        f.write(f'os_release = {platform.release()}\n')
        f.write(f'os_version = {platform.version()}\n')
        f.write(f'os_platform = {platform.platform()}\n')


def main():
    os.makedirs(f'{ALLURE_RESULTS_DIR}/history', exist_ok=True)
    os.system(f'cp -ruvT {ALLURE_REPORT_DIR}/history/ {ALLURE_RESULTS_DIR}/history/')
    os.system(f'pytest --alluredir {ALLURE_RESULTS_DIR}')
    create_environment_properties()
    create_executor_json()    
    os.system(f'allure generate -o {ALLURE_REPORT_DIR} --clean --name {$project_name}')


if __name__ == '__main__':
    main()
