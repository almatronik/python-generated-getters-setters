#!/usr/bin/env python3

import os

PRODUCED_CODE_PATH = "../test"
PRODUCED_CODE_FILENAME = "test.cpp"
PRODUCED_CODE_FULLPATH = os.path.join(PRODUCED_CODE_PATH, PRODUCED_CODE_FILENAME)
MODULE_NAME = os.path.splitext(os.path.basename(PRODUCED_CODE_FILENAME))[0]

def generate(defines, signals):
    if not os.path.isdir(PRODUCED_CODE_PATH):
        os.mkdir(PRODUCED_CODE_PATH)

    output = ""
#============================================================================================
    output += f'#include "signals.h"\n'
    output += f'#include "gtest/gtest.h"\n\n'

    for i in range(len(signals)):
        output += f"TEST(signal_test, {signals[i]['name']})\n"
        output += f"{{\n"
        output += f"    {signals[i]['type']} value;\n\n"
        if 'range' in signals[i]:
            for j in range(len(signals[i]['range'])):
                output += f"    value = {signals[i]['range'][j]};\n"
                output += f"    EXPECT_TRUE(signals_set_{signals[i]['name']}(value));\n"
                output += f"    EXPECT_EQ(value, signals_get_{signals[i]['name']}());\n\n"

            output += f"    value = {signals[i]['range'][1]} + 1;\n"
            output += f"    EXPECT_FALSE(signals_set_{signals[i]['name']}(value));\n"

            if signals[i]['type'] == "float" or signals[i]['type'] == "int8_t" or signals[i]['type'] == "int16_t" or signals[i]['type'] == "int32_t" or signals[i]['range'][0] > 0:
                output += f"\n    value = {signals[i]['range'][0]} - 1;\n"
                output += f"    EXPECT_FALSE(signals_set_{signals[i]['name']}(value));\n"

        elif signals[i]['values'] == "status":
            for j in range(len(defines['status'])):
                output += f"    value = {defines['status'][j]};\n"
                output += f"    EXPECT_TRUE(signals_set_{signals[i]['name']}(value));\n"
                output += f"    EXPECT_EQ(value, signals_get_{signals[i]['name']}());\n\n"

            output += f"    value = {defines['status'][-1]} + 1;\n"
            output += f"    EXPECT_FALSE(signals_set_{signals[i]['name']}(value));\n"

        elif signals[i]['values'] == "states":
            for j in range(len(defines['states'])):
                output += f"    value = {defines['states'][j]};\n"
                output += f"    EXPECT_TRUE(signals_set_{signals[i]['name']}(value));\n"
                output += f"    EXPECT_EQ(value, signals_get_{signals[i]['name']}());\n\n"

            output += f"    value = {defines['states'][-1]} + 1;\n"
            output += f"    EXPECT_FALSE(signals_set_{signals[i]['name']}(value));\n"
        
        output += f"}}\n\n"
#============================================================================================
    with open(PRODUCED_CODE_FULLPATH, 'w') as f:
        f.write(output)