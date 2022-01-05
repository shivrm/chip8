import toml
import re

with open("./src/utils/instr.toml", "r") as f:
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

        args_str = match.groups()
        args_int = [int(arg, 16) for arg in args_str]

        return opcode, args_int

    else:
        return None
