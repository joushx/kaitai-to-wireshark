#!/bin/bash

if [ "$#" != "2" ]; then
    echo "Usage: test.sh <definition> <data>"
    exit 1
fi

definition=$1
data=$2

# generate dissector from format definition
python3 convert.py "kaitai_struct_tests/formats/$definition.ksy" > "/tmp/$definition.lua" &&

# convert test data to hex dump
od -Ax -tx1 -v "kaitai_struct_tests/src/$data" > /tmp/dump &&

# convert hex dump to pcap file
text2pcap -l 162 /tmp/dump /tmp/example.pcap &&

# parse pcap file using tshark and generated dissector
tshark -r /tmp/example.pcap -X "lua_script:/tmp/$definition.lua" -o "uat:user_dlts:\"User 15 (DLT=162)\",\"$definition\",\"0\",\"\",\"0\",\"\"" -T json
