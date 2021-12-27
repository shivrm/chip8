import toml
import re

with open("./src/instr.toml", "r") as f:
    data = toml.load(f)

regexed = {}
for instr, hex in data.items():
    regexed_hex = (
        hex.replace("nnn", "([0-9a-f]{3})")
        .replace("x", "([0-9a-f])")
        .replace("y", "([0-9a-f])")
        .replace("n", "([0-9a-f])")
    )
    regexed[instr] = regexed_hex


def instr_parse(instruction):
    for instr, hex in regexed.items():
        match = re.match(hex, instruction)
    
        if not match:
            continue
        
        print(instr, match.groups())
        break
    
    else:
        print("No matches")