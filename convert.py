#!/usr/bin/env python3

from yaml import load, dump
from jinja2 import Template
import sys

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# load definition file into string
definition_file = sys.argv[1]
definition = open(definition_file).read()

# parse definition yaml
ksy = load(definition, Loader=Loader)

# read template
template = open("templates/template.lua").read()

# generate output
template = Template(template,trim_blocks=True,lstrip_blocks=True)

# print result
print(template.render(data=ksy))
