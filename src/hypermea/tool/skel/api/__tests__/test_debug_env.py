# __tests__/test_debug_env.py
import sys
import os

def test_debug_env():
    print("\n\n--- DEBUG INFO ---")
    print(' > this is not a test, rather information that may help troubleshoot issues running tests')
    print("sys.path:        ", sys.path)
    print("executable:      ", sys.executable)
    print("env PYTHONPATH:  ", os.environ.get("PYTHONPATH"))
    print("env VIRTUAL_ENV: ", os.environ.get("VIRTUAL_ENV"))
    print("------------------\n\n")
