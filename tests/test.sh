#!/bin/bash
set -x

DEFINITION=$1
DATA=$2

python3 convert.py kaitai_struct_tests/formats/$DEFINITION.ksy > /tmp/$DEFINITION.lua &&
od -Ax -tx1 -v kaitai_struct_tests/src/$DATA > /tmp/dump &&
text2pcap -l 162 /tmp/dump /tmp/example.pcap &&
tshark -r /tmp/example.pcap -X lua_script:/tmp/$DEFINITION.lua -o "uat:user_dlts:\"User 15 (DLT=162)\",\"$DEFINITION\",\"0\",\"\",\"0\",\"\"" -T json