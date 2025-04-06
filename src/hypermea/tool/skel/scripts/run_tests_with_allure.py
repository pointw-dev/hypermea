#!/usr/bin/env python

import os
import json
import sys
from pathlib import Path

# Add src/service to sys.path to allow `from configuration import ...` to work
service_dir = Path(__file__).resolve().parents[1] / "service"
sys.path.insert(0, str(service_dir))

from hypermea.core.utils import get_operating_environment

ALLURE_RESULTS_DIR = './allure-results'
ALLURE_REPORT_DIR = "./allure-report"


def create_executor_json():
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

    executor = {
        'name': 'run_tests_with_allure.py',
        'type': 'python script',
        'buildName': 'manually built'
    }
    with open(f'{ALLURE_RESULTS_DIR}/executor.json', 'w', encoding='utf8') as f:
        json.dump(executor, f, indent=4)


def create_environment_properties():
    """
    environment.properties

    os_platform = linux
    os_release = 5.15.0-60-generic
    os_version = #66-Ubuntu SMP Fri Jan 20 14:29:49 UTC 2023
    python_version = Python 3.10.9
    """

    op_env = get_operating_environment()
    with open(f'{ALLURE_RESULTS_DIR}/environment.properties', 'w', encoding='utf8') as f:
        for component, version in op_env['versions'].items():
            f.write(f'{component} = {version}\n')

        for group in op_env['settings_groups']:
            for setting, value in group['settings'].items():
                f.write(f'{setting} = {value}\n')



def main():
    os.environ['ALLURE_NO_ANALYTICS'] = '1'
    os.makedirs(f'{ALLURE_RESULTS_DIR}/history', exist_ok=True)
    os.system(f'cp -ruvT {ALLURE_REPORT_DIR}/history/ {ALLURE_RESULTS_DIR}/history/')
    os.system(f'pytest --alluredir {ALLURE_RESULTS_DIR}')
    create_environment_properties()
    create_executor_json()
    os.system(f'cp favicon.ico {ALLURE_REPORT_DIR}')    
    os.system(f'allure generate -o {ALLURE_REPORT_DIR} --clean --name {$project_name}')


if __name__ == '__main__':
    main()
