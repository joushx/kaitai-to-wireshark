#!/usr/bin/env python3

import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import json
import subprocess

TESTS_DIR = "./kaitai_struct_tests"
DEFINITION_DIR = TESTS_DIR + "/spec/ks/"

def load_tests():
    definition_files = os.listdir(DEFINITION_DIR)
    return [load_test(f) for f in definition_files]

def load_test(filename):
    file_contents = open(DEFINITION_DIR + filename).read()
    return yaml.load(file_contents, Loader=Loader)

def pytest_generate_tests(metafunc):
    if "definition" in metafunc.fixturenames:
        tests = load_tests()
        metafunc.parametrize("definition", tests)

def test_output(definition):
    result = subprocess.run(['bash', './tests/test.sh', definition["id"], definition["data"]], capture_output=True, text=True)
    result = json.loads(result.stdout)[0]["_source"]["layers"][definition["id"]]["_ws.lua.text"]
    print(result)

    for a in definition["asserts"]:
        expected = a["expected"]
        actual = result[definition["id"] + "." + a["actual"]]

        assert expected == actual