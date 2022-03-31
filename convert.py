#!/usr/bin/env python3

from yaml import load, dump
from jinja2 import Template
import sys

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

ksy = load(open(sys.argv[1]).read(), Loader=Loader)
template = open("templates/template.lua").read()

template = Template(template,trim_blocks=True,lstrip_blocks=True)
print(template.render(data=ksy))
