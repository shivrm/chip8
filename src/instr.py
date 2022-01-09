import re
import toml

def cls(cpu):
    cpu.display.clear()

def call(cpu, mem):
    """Calls a subroutine

    Args:
        mem (int12): The memory address of the subroutine to call
    """
    
    if cpu.registers.SP == 15:
        # Stack Overflow
        return
    
    cpu.stack[cpu.registers.SP] = cpu.registers.PC
    cpu.registers.SP += 1
    
    cpu.registers.PC = mem
    
def ret(cpu):
    """Returns from a subroutine back to the parent process
    """
    
    if cpu.registers.SP == 0:
        # Stack Underflow
        return
    
    cpu.registers.SP -= 1
    cpu.registers.PC = cpu.stack[cpu.registers.CP]
    
def ld1(cpu, reg, value):
    """Loads a constant value into a register

    Args:
        reg (int4): The index of the register into which the value is loaded
        value (int8): A constant value
    """
    cpu.registers.V[reg] = value


def ld2(cpu, reg1, reg2):
    """Loads the value of one register into another

    Args:
        reg1 (int4): The index of the register to which the value is loaded
        reg2 (int4): The index of the register from which the value is loaded
    """
    cpu.registers.V[reg1] = cpu.registers.V[reg2]


def ld3(cpu, mem):
    """Loads a 12 bit value into the I register

    Args:
        mem (int12): The value to load into I
    """
    cpu.registers.I = mem


def ld4(cpu, reg):
    """Loads the value of DT into a register

    Args:
        reg (int4): The index of the register into which the value is loaded
    """
    cpu.registers.V[reg] = cpu.registers.DT

def ld5(cpu, reg):
    """Loads the value of the pressed key into a register.
    Waits until a key is pressed

    Args:
        reg (int4): The index of the register into which the value is loaded
    """
    if not any(cpu.display.pressed_keys):
        cpu.registers.PC -= 1
        return
    
    cpu.registers.V[reg] = cpu.display.pressed_keys.index(True)

def ld6(cpu, reg):
    """Loads the value of a register into DT

    Args:
        reg (int4): The index of the register from which the value is loaded
    """
    cpu.registers.DT = cpu.registers.V[reg]


def ld7(cpu, reg):
    """Loads the value of a register into ST

    Args:
        reg (int4): The index of the register from which the value is loaded
    """
    cpu.registers.ST = cpu.registers.V[reg]


def ld8(cpu, value):
    """Set the I register to the memory location where the sprite
    for the digit corresponding to 'value' is stored

    Args:
        value (int4): The hex digit the sprite corresponds to
    """
    cpu.registers.I = value * 5


def ld9(cpu, reg):
    """Loads the BCD representation of the value in a register into
    the memory addresses at I, I+1 and I+2

    Args:
        reg (int4): The index of the register whose BCD representation is to be taken
    """
    val = cpu.registers.V[reg]
    digits = val // 100, val // 10 % 10, val % 10

    for idx, digit in enumerate(digits):
        memloc = cpu.registers.I + idx
        cpu.memory[memloc] = digit


def ld10(cpu, reg):
    """Loads registers V0 through V(reg - 1) with the values in memory from
    I to I + (reg - 1)

    Args:
        reg (int4): The index of the register upto which values are loaded
    """
    for idx in range(cpu, reg):
        memloc = cpu.registers.I + idx
        cpu.registers.V[idx] = cpu.memory[memloc]


def ld11(cpu, reg):
    """Sets the value at memory locations I through I + (reg - 1) from
    registers V0 through V(reg - 1)

    Args:
        reg (int4): The index of the register upto which values are loaded
    """
    for idx in range(cpu, reg):
        memloc = cpu.registers.I + idx
        cpu.memory[memloc] = cpu.registers.V[idx]


def add1(cpu, reg, value):
    added = cpu.registers.V[reg] + value
    cpu.registers.V[reg] = added % 256


def add2(cpu, reg1, reg2):
    added = cpu.registers.V[reg1] + cpu.registers.V[reg2]
    cpu.registers.VF = int(added > 255)
    cpu.registers.V[reg1] = added % 256


def add3(cpu, reg):
    added = cpu.registers.I + cpu.registers.V[reg]
    cpu.registers.I = added % 65536


def sub(cpu, reg1, reg2):
    subbed = cpu.registers.V[reg1] - cpu.registers.V[reg2]
    cpu.registers.VF = subbed >= 0
    cpu.registers.V[reg1] = subbed


def subn(cpu, reg1, reg2):
    subbed = cpu.registers.V[reg2] - cpu.registers.V[reg1]
    cpu.registers.VF = subbed >= 0
    cpu.registers.V[reg2] = subbed


def jp1(cpu, mem):
    cpu.registers.PC = mem


def jp2(cpu, mem):
    cpu.registers.PC = mem + cpu.registers.V[0]


def se1(cpu, reg, value):
    if cpu.registers.V[reg] == value:
        cpu.registers.PC += 1


def se2(cpu, reg1, reg2):
    if cpu.registers.V[reg1] == cpu.registers.V[reg2]:
        cpu.registers.PC += 1


def sne1(cpu, reg, value):
    if cpu.registers.V[reg] != value:
        cpu.registers.PC += 1


def sne2(cpu, reg1, reg2):
    if cpu.registers.V[reg1] != cpu.registers.V[reg2]:
        cpu.registers.PC += 1


def skp(cpu, reg):
    key_to_test = cpu.registers.V[reg]
    
    if cpu.display.pressed_keys[key_to_test]:
        cpu.registers.PC += 1

def sknp(cpu, reg):
    key_to_test = cpu.registers.V[reg]
    
    if not cpu.display.pressed_keys[key_to_test]:
        cpu.registers.PC += 1

def o_r(cpu, reg1, reg2):
    value = cpu.registers.V[reg1] | cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def and_(cpu, reg1, reg2):
    value = cpu.registers.V[reg1] & cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def xor(cpu, reg1, reg2):
    value = cpu.registers.V[reg1] ^ cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def shr(cpu, reg1, reg2):
    if cpu.registers.V[reg1] & 1:
        cpu.registers.VF = 1

    value = cpu.registers.V[reg1] >> 1
    cpu.registers.V[reg1] = value


def shl(cpu, reg1, reg2):
    if cpu.registers.V[reg1] & 128:
        cpu.registers.VF = 1

    value = cpu.registers.V[reg1] << 1
    cpu.registers.V[reg1] = value
  
#########################################
  
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


def parse(instruction):
    for opcode, hex in patterns.items():
        match = re.match(hex, instruction)

        if not match:
            continue

        args_str = match.groups()
        args_int = [int(arg, 16) for arg in args_str]

        return opcode, args_int

    else:
        return None
