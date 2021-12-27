import toml
import re

with open("./src/instr.toml", "r") as f:
    oper_dict = toml.load(f)

patterns = {}
for opcode, hex in oper_dict.items():
    hex_regex = (
        hex.replace("nnn", "([0-9a-f]{3})")
        .replace("x", "([0-9a-f])")
        .replace("y", "([0-9a-f])")
        .replace("n", "([0-9a-f])")
    )
    patterns[opcode] = hex_regex


def instr_parse(instruction):
    for opcode, hex in patterns.items():
        match = re.match(hex, instruction)
    
        if not match:
            continue
        
        return opcode, match.groups()
    
    else:
        return None