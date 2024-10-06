#!/usr/bin/env python3

import json
import os

PATH = "../lib/signals"
SOURCE = "signals.cpp"
FILEPATH = os.path.join(PATH, SOURCE)

def generate_source():
    with open('data.json', 'r') as file:
        data = json.load(file)

    defines = data['defines']
    signals = data['signals']

    if not os.path.isdir(PATH):
        os.mkdir(PATH)
    db = open(FILEPATH, "w")

# ----------------------UPPER BODY--------------------------
    db.write('''\
#include "buffer.h"
#include "signals.h"

static constexpr float PRECISION{0.1F};

static uint8_t buffer[16]{0};

''')

# ----------------------FUNCTIONS--------------------------
    for i in range(len(signals)):
        db.write(f"bool signals_set_{signals[i]['name']}({signals[i]['type']} value)\n")
        db.write(f"{{\n")
        db.write(f"    bool status{{false}};\n")
        if 'range' in signals[i]:
            db.write(f"    if((value >= {signals[i]['range'][0]}) && (value <= {signals[i]['range'][1]}))\n")
        elif signals[i]['values'] == "status":
            db.write(f"    if(value <= {defines['status'][-1]})\n")
        elif signals[i]['values'] == "states":
            db.write(f"    if(value <= {defines['states'][-1]})\n")
        db.write(f"    {{\n")
        db.write(f"        status = true;\n")
        if signals[i]['type'] == 'float':
            db.write(f"        buffer_insert(buffer, {signals[i]['start']}, {signals[i]['length']}, value / PRECISION);\n")
        else:
            db.write(f"        buffer_insert(buffer, {signals[i]['start']}, {signals[i]['length']}, value);\n")
        db.write(f"    }}\n")
        db.write(f"    return status;\n")
        db.write(f"}}\n\n")
        db.write(f"{signals[i]['type']} signals_get_{signals[i]['name']}(void)\n")
        db.write(f"{{\n")
        if signals[i]['type'] == 'float':
            db.write(f"    return (PRECISION * buffer_extract(buffer, {signals[i]['start']}, {signals[i]['length']}));\n")
        elif not (signals[i]['type'] == 'int8_t' or signals[i]['type'] == 'int16_t' or signals[i]['type'] == 'int32_t'):
            db.write(f"    return ({signals[i]['type']})buffer_extract(buffer, {signals[i]['start']}, {signals[i]['length']});\n")
        elif (signals[i]['type'] == 'int8_t' or signals[i]['type'] == 'int16_t' or signals[i]['type'] == 'int32_t'):
            db.write(f"    {signals[i]['type']} tmp = ({signals[i]['type']})buffer_extract(buffer, {signals[i]['start']}, {signals[i]['length']});\n")
            db.write(f"    if (tmp >> {signals[i]['length'] - 1} == 1)\n")
            db.write(f"    {{\n")
            db.write(f"        std::size_t size{{{signals[i]['length']}}};\n")
            db.write(f"        int bin[size]{{0}};\n")
            db.write(f"        for (int i = 0; i < size; i++)\n")
            db.write(f"        {{\n")
            db.write(f"            bin[i] = tmp % 2;\n")
            db.write(f"            tmp = tmp / 2;\n")
            db.write(f"        }}\n")
            db.write(f"        for (int i = 0; i < size; i++)\n")
            db.write(f"        {{\n")
            db.write(f"            if (bin[i] == 0)\n")
            db.write(f"            {{\n")
            db.write(f"                bin[i] = 1;\n")
            db.write(f"            }}\n")
            db.write(f"            else\n")
            db.write(f"            {{\n")
            db.write(f"                bin[i] = 0;\n")
            db.write(f"            }}\n")
            db.write(f"        }}\n")
            db.write(f"        for (int i = size - 1; i >= 0; i--)\n")
            db.write(f"        {{\n")
            db.write(f"            tmp *= 2;\n")
            db.write(f"            tmp += bin[i];\n")
            db.write(f"        }}\n")
            db.write(f"        tmp += 1;\n")
            db.write(f"        tmp *= -1;\n")
            db.write(f"    }}\n")
            db.write(f"    return tmp;\n")
        
        if i < len(signals) - 1:
            db.write(f"}}\n\n")
        else:
            db.write(f"}}")
    db.close()
