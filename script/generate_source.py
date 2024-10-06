#!/usr/bin/env python3

import os

PRODUCED_CODE_PATH = "../lib/signals"
PRODUCED_CODE_FILENAME = "signals.cpp"
PRODUCED_CODE_FULLPATH = os.path.join(PRODUCED_CODE_PATH, PRODUCED_CODE_FILENAME)
MODULE_NAME = os.path.splitext(os.path.basename(PRODUCED_CODE_FILENAME))[0]

def generate(defines, signals):
    if not os.path.isdir(PRODUCED_CODE_PATH):
        os.mkdir(PRODUCED_CODE_PATH)
    output = ""
# ----------------------UPPER BODY--------------------------
    output += f'#include "buffer.h"\n'
    output += f'#include "signals.h"\n\n'
    output += f"static constexpr float PRECISION{{0.1F}};\n\n"
    output += f"static uint8_t buffer[16]{{0}};\n\n"
# ----------------------FUNCTIONS--------------------------
    for i in range(len(signals)):
        output += f"bool signals_set_{signals[i]['name']}({signals[i]['type']} value)\n"
        output += f"{{\n"
        output += f"    bool status{{false}};\n"
        if 'range' in signals[i]:
            output += f"    if((value >= {signals[i]['range'][0]}) && (value <= {signals[i]['range'][1]}))\n"
        elif signals[i]['values'] == "status":
            output += f"    if(value <= {defines['status'][-1]})\n"
        elif signals[i]['values'] == "states":
            output += f"    if(value <= {defines['states'][-1]})\n"
        output += f"    {{\n"
        output += f"        status = true;\n"
        if signals[i]['type'] == 'float':
            output += f"        buffer_insert(buffer, {signals[i]['start']}, {signals[i]['length']}, value / PRECISION);\n"
        else:
            output += f"        buffer_insert(buffer, {signals[i]['start']}, {signals[i]['length']}, value);\n"
        output += f"    }}\n"
        output += f"    return status;\n"
        output += f"}}\n\n"
        output += f"{signals[i]['type']} signals_get_{signals[i]['name']}(void)\n"
        output += f"{{\n"
        if signals[i]['type'] == 'float':
            output += f"    return (PRECISION * buffer_extract(buffer, {signals[i]['start']}, {signals[i]['length']}));\n"
        elif not (signals[i]['type'] == 'int8_t' or signals[i]['type'] == 'int16_t' or signals[i]['type'] == 'int32_t'):
            output += f"    return ({signals[i]['type']})buffer_extract(buffer, {signals[i]['start']}, {signals[i]['length']});\n"
        elif (signals[i]['type'] == 'int8_t' or signals[i]['type'] == 'int16_t' or signals[i]['type'] == 'int32_t'):
            output += f"    {signals[i]['type']} tmp = ({signals[i]['type']})buffer_extract(buffer, {signals[i]['start']}, {signals[i]['length']});\n"
            output += f"    if (tmp >> {signals[i]['length'] - 1} == 1)\n"
            output += f"    {{\n"
            output += f"        std::size_t padding{{{int (''.join(filter(str.isdigit, signals[i]['type'])))} - {signals[i]['length']}}};\n"
            output += f"        tmp = (~tmp) + 1;\n"
            output += f"        tmp = tmp << padding;\n"
            output += f"        tmp = tmp >> padding;\n"
            output += f"        tmp *= -1;\n"
            output += f"    }}\n"
            output += f"    return tmp;\n"
        
        if i < len(signals) - 1:
            output += f"}}\n\n"
        else:
            output += f"}}"

    with open(PRODUCED_CODE_FULLPATH, 'w') as f:
        f.write(output)