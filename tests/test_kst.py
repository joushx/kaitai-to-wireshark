#!/usr/bin/env python3

import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import json
import subprocess
import pytest

TESTS_DIR = "./kaitai_struct_tests"
DEFINITION_DIR = TESTS_DIR + "/spec/ks/"

def load_tests():
    definition_files = os.listdir(DEFINITION_DIR)
    #definition_files = ["user_type.kst", "str_encodings.kst"]
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
    dict = json.loads(result.stdout)

    # unknown why this happens
    result = {}
    if "_ws.lua.text" in dict[0]["_source"]["layers"][definition["id"]]:
        result = dict[0]["_source"]["layers"][definition["id"]]["_ws.lua.text"]
    else:
        result = dict[0]["_source"]["layers"][definition["id"]]
    

    # Wireshark uses "types.value" (e.g. header.width) for fields,
    # Kaitai uses "instance.value" (e.g. header_one.width). Thus, we cannot compare the fields
    # with the same name with each other.
    actual_values = list(result.values())
    expected_values = [str(a["expected"]) for a in definition["asserts"]]

    for value in expected_values:

        # remove quotes from strings
        if value[0] == "\"" and value[-1] == "\"":
            value = value[1:-1]
            
        if value not in actual_values:
            pytest.fail("Expected value '" + str(value) + "' is not in actual values " + str(actual_values))