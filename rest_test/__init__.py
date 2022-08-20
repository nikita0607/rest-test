#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse

from ._parser import YAMLParser
from ._results import RestPassed

__all__ = ["checkers", "_parser"]


def run():
    try:
        _run()
    except FileNotFoundError:
        pass


def _run():
    description = "Description"
    usage = "rest-test PATH_TO_FILE(s)"

    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument("path", help="Parg to test file(s)")

    namespace = parser.parse_args()
    
    path = namespace.path
    
    if path[0] not in ("~", "/"):
        path = f"{os.getcwd()}/{path}"

    yamlparser = YAMLParser(path)

    
    for res in yamlparser.run_checkers():
        test_name = f"TestName: ---{res.checker.name}---"
        
        print(test_name)
        if isinstance(res, RestPassed):
            print("Status: PASSED")
        else:
            print("Status: ERROR:")
            print(f"Expected response: {res.test_response}")
            print(f"Server response: {res.server_response}")
        print("_"*len(test_name))
        print()


if __name__ == "__main__":
    pass

