#!/usr/bin/env python3

import json

JSON_FILE = "./data.json"

with open(JSON_FILE, 'r') as file:
    data = json.load(file)

defines = data['defines']
signals = data['signals']

import generate_header
import generate_source
import generate_test
import generate_list

generate_header.generate(defines, signals)
generate_source.generate(defines, signals)
generate_test.generate(defines, signals)
generate_list.generate(defines, signals)