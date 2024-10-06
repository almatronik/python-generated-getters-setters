#!/usr/bin/env python3

import os

PRODUCED_CODE_PATH = "../lib/signals"
PRODUCED_CODE_FILENAME = "signals.h"
PRODUCED_CODE_FULLPATH = os.path.join(PRODUCED_CODE_PATH, PRODUCED_CODE_FILENAME)
# PRODUCED_CODE_FULLPATH = (PRODUCED_CODE_PATH) + "/" + (PRODUCED_CODE_FILENAME)
MODULE_NAME = os.path.splitext(os.path.basename(PRODUCED_CODE_FILENAME))[0]

def generate(defines, signals):
    if not os.path.isdir(PRODUCED_CODE_PATH):
        os.mkdir(PRODUCED_CODE_PATH)
    output = ""
#============================================================================================
    output += f"#ifndef {MODULE_NAME}_H\n"
    output += f"#define {MODULE_NAME}_H\n\n"
    output += f"#include <cstdint>\n\n"

    for i, row in enumerate(defines):
        for j, value in enumerate(defines[row]):
            output += f"#define {value} {j}\n"
    output += f"\n"

    for i in range(len(signals)):
        output += f"/**\n"
        output += f" * @brief This function is used to set {signals[i]['comment']}\n"
        output += f"\n *\n"
        if 'range' in signals[i]:
            output += f" * @param value The valid {signals[i]['name']} range [{signals[i]['range'][0]} - {signals[i]['range'][1]}]\n"
        elif signals[i]['values'] == 'status':
            output += f" * @param value The valid statuses: {defines['status'][0]}, {defines['status'][1]}, {defines['status'][2]}\n"
        elif signals[i]['values'] == 'states':
            output += f" * @param value The valid states: {defines['states'][0]}, {defines['states'][1]}\n"
        else:
            output += f"ERROR: MISSING LINE\n"
        output += f" * @return bool True if value was successfully set, False otherwise.\n"
        output += f" */\n"
        output += f"bool signals_set_{signals[i]["name"]}({signals[i]['type']} value);\n\n"


        output += f"/**\n"
        output += f" * @brief This function is used to get {signals[i]["comment"]}\n *\n"
        output += f" * @return {signals[i]['type']} Value of {signals[i]['comment']}\n*/\n"
        output += f"{signals[i]['type']} signals_get_{signals[i]['name']}(void);\n\n"

    output += f"#endif //{MODULE_NAME}"

    with open(PRODUCED_CODE_FULLPATH, 'w') as f:
        f.write(output)