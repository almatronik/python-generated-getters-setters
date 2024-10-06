#!/usr/bin/env python3

import os

PRODUCED_CODE_PATH = "../lib/signals"
PRODUCED_CODE_FILENAME = "signals.txt"
PRODUCED_CODE_FULLPATH = os.path.join(PRODUCED_CODE_PATH, PRODUCED_CODE_FILENAME)

def generate(defines, signals):
    if not os.path.isdir(PRODUCED_CODE_PATH):
        os.mkdir(PRODUCED_CODE_PATH)
    output = ""
#============================================================================================
    title = {"name": "Signal", "type": "Type", "values": "Values", "comment": "Description"}

    size = {}
    for key in title:
        if key == 'values':
            size[key] = len(title['values']) # Necessary evil here. I had to hardcode 'values' for the time being.
        elif key == 'range':
            size[key] = len(title['values']) # Necessary evil here. I had to hardcode 'values' for the time being.
        else:
            size[key] = len(title[key])

    for signal in signals:
        for key in signal:
            if key == 'start' or key == 'length':
                pass
            elif key == 'values':
                length = len(str(signal[key]))
                if size[key] < length:
                    size[key] = length
                if length < len(str(defines['status'])):
                    length = len(str(defines['status'])) - 7
                    size[key] = length
            elif key == 'range':
                length = len(str(signal[key][0]) + ", " + str(signal[key][1]))
                
                if size['values'] < length: # Necessary evil here. I had to hardcode 'values' for the time being.
                    size['values'] = length # Necessary evil here. I had to hardcode 'values' for the time being.
            else:
                length = len(str(signal[key]))
                if size[key] < length:
                    size[key] = length

    output += f"({title['name'].ljust(size['name'])} | {title['type'].ljust(size['type'])} | {title['values'].ljust(size['values'])} | {title['comment'].ljust(size['comment'])})\n"
    output += '-' * (sum(size.values()) + 9)
    output += "\n"

    for signal in signals:
        output += f"{signal['name'].ljust(size['name'])} | {signal['type'].ljust(size['type'])} | "
        if 'range' in signal:
            output += f"[{signal['range'][0]}, {signal['range'][1]}] " .ljust(size['values'])
            output += " | "
        elif signal['values'] == "status":
            output += f"[{defines['status'][0]} {defines['status'][1]} {defines['status'][2]}] ".ljust(size['values'])
            output += " | "
        elif signal['values'] == "states":
            output += f"[{defines['states'][0]} {defines['states'][1]}] ".ljust(size['values'])
            output += " | "
        output += f"{signal['comment'].capitalize().ljust(size['comment'])}\n"
#============================================================================================
    with open(PRODUCED_CODE_FULLPATH, 'w') as f:
        f.write(output)