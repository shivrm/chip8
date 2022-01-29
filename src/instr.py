import re
from pygame import sprite
import toml
from random import randint


def cls(cpu):
    """Clears the display"""
    cpu.display.clear()


def drw(cpu, reg_x, reg_y, num_bytes):
    x_start = cpu.registers.V[reg_x]
    y_start = cpu.registers.V[reg_y]
    
    for byte_idx in range(num_bytes):
        row = (y_start + byte_idx) % 32
        sprite_val = cpu.memory[cpu.registers.I + byte_idx]
        
        for col_offset in range(8):
            set_bit = sprite_val & (128 >> col_offset)
            col = (x_start + col_offset) % 64
            
            if set_bit:
                cpu.registers.V[15] = (cpu.display.flip(col, row)
                                       or cpu.registers.V[15])
        
def call(cpu, mem_addr):
    """Calls a subroutine

    Args:
        mem_addr (int12): The memory address of the subroutine to call
    """

    # Ensure that stack size does not exceed 16
    if cpu.registers.SP == 15:
        # Stack Overflow
        return

    # Push the current memory location onto the stack
    cpu.stack[cpu.registers.SP] = cpu.registers.PC
    cpu.registers.SP += 1

    # Set the program counter to the new location
    cpu.registers.PC = mem_addr - 2


def ret(cpu):
    """Returns from a subroutine back to the parent process"""

    # Ensure that the stack is not empty
    if cpu.registers.SP == 0:
        # Stack Underflow
        return

    # Pop the topmost value and store it in the program counter
    cpu.registers.SP -= 1
    cpu.registers.PC = cpu.stack[cpu.registers.SP]


def ld1(cpu, register, value):
    """Loads a constant value into a register

    Args:
        register (int4): The index of the register into which the value is loaded
        value (int8): A constant value
    """
    cpu.registers.V[register] = value


def ld2(cpu, reg_to, reg_from):
    """Loads the value of one register into another

    Args:
        reg_to (int4): The index of the register to which the value is loaded
        reg_from (int4): The index of the register from which the value is loaded
    """
    cpu.registers.V[reg_to] = cpu.registers.V[reg_from]


def ld3(cpu, value):
    """Loads a 12 bit value into the I register

    Args:
        value (int12): The value to load into I
    """
    cpu.registers.I = value


def ld4(cpu, register):
    """Loads the value of DT into a register

    Args:
        register (int4): The index of the register into which the value is loaded
    """
    cpu.registers.V[register] = cpu.registers.DT


def ld5(cpu, register):
    """Loads the value of the pressed key into a register.
    Waits until a key is pressed

    Args:
        register (int4): The index of the register into which the value is loaded
    """

    # While no keys are pressed, keep returning to this instruction
    if not any(cpu.display.pressed_keys):
        cpu.registers.PC -= 2
        return

    # Set the register to the first pressed key in the list
    cpu.registers.V[register] = cpu.display.pressed_keys.index(True)


def ld6(cpu, register):
    """Loads the value of a register into DT

    Args:
        register (int4): The index of the register from which the value is loaded
    """
    cpu.registers.DT = cpu.registers.V[register]


def ld7(cpu, register):
    """Loads the value of a register into ST

    Args:
        register (int4): The index of the register from which the value is loaded
    """
    cpu.registers.ST = cpu.registers.V[register]


def ld8(cpu, reg):
    """Set the I register to the memory location where the sprite
    for the digit corresponding to 'digit' is stored

    Args:
        digit (int4): The hex digit the sprite corresponds to
    """

    # Since the sprites are stored starting at memory address 0,
    # And each sprite occupies 5 bytes, we can obtain the location
    # of the sprite by multiplying the corresponding digit by 5
    print(cpu.registers.V[0])
    
    digit = cpu.registers.V[reg] % 16
    cpu.registers.I = digit * 5
    
    print(cpu.registers.I, cpu.memory[cpu.registers.I: cpu.registers.I + 6])


def ld9(cpu, register):
    """Loads the BCD representation of the value in a register into
    the memory addresses at I, I+1 and I+2

    Args:
        register (int4): The index of the register whose BCD representation is to be taken
    """

    # Split the value of the register into 3 digits
    val = cpu.registers.V[register]
    digits = val // 100, val // 10 % 10, val % 10

    # Store the digits at memory addresses I, I+1 and I+2
    for idx, digit in enumerate(digits):
        memloc = cpu.registers.I + idx
        cpu.memory[memloc] = digit
        
        
def ld10(cpu, register):
    """Sets the value at memory locations I through I + (register - 1) from
    registers V0 through V(register - 1)

    Args:
        register (int4): The index of the register upto which values are loaded
    """

    # Loop with idx = 0 through reg - 1. Get the memory address and store
    # the value of each register at the memory addresses
    for idx in range(register + 1):
        memloc = cpu.registers.I + idx
        cpu.memory[memloc] = cpu.registers.V[idx]


def ld11(cpu, register):
    """Loads registers V0 through V(register - 1) with the values in memory from
    I to I + (register - 1)

    Args:
        register (int4): The index of the register upto which values are loaded
    """

    # Loop with idx = 0 through reg - 1. Get the memory address and load
    # the register with the value at that address
    for idx in range(register + 1):
        memloc = cpu.registers.I + idx
        cpu.registers.V[idx] = cpu.memory[memloc]


def add1(cpu, register, value):
    """Adds a constant value to a register

    Args:
        register (int4): The index of the register to which the value is added
        value (int8): The value that is added
    """
    added = cpu.registers.V[register] + value
    cpu.registers.V[register] = added % 256


def add2(cpu, reg_to, reg_from):
    """Adds the value of one register into another

    Args:
        reg_to (int4): The index of the register to which the value is added
        reg_from (int4): The index of the register whose value is added
    """
    
    # Add the two values and set VF if there is an overflow
    added = cpu.registers.V[reg_to] + cpu.registers.V[reg_from]
    cpu.registers.V[15] = added > 255
    
    # Load the value, mod 256, into reg_to
    cpu.registers.V[reg_to] = added % 256


def add3(cpu, register):
    """Adds the value of a register into the I register

    Args:
        register (int4): The register whose value is added
    """
    
    # Add the values, and load it into the I register, mod 65536
    added = cpu.registers.I + cpu.registers.V[register]
    cpu.registers.I = added % 65536


def sub(cpu, reg1, reg2):
    subbed = cpu.registers.V[reg1] - cpu.registers.V[reg2]
    cpu.registers.V[15] = subbed >= 0
    cpu.registers.V[reg1] = subbed % 256


def subn(cpu, reg1, reg2):
    subbed = cpu.registers.V[reg2] - cpu.registers.V[reg1]
    cpu.registers.V[15] = subbed >= 0
    cpu.registers.V[reg2] = subbed % 256


def jp1(cpu, mem):
    cpu.registers.PC = mem - 2


def jp2(cpu, mem):
    cpu.registers.PC = mem + cpu.registers.V[0] - 2


def se1(cpu, reg, value):
    if cpu.registers.V[reg] == value:
        cpu.registers.PC += 2


def se2(cpu, reg1, reg2):
    if cpu.registers.V[reg1] == cpu.registers.V[reg2]:
        cpu.registers.PC += 2


def sne1(cpu, reg, value):
    if cpu.registers.V[reg] != value:
        cpu.registers.PC += 2


def sne2(cpu, reg1, reg2):
    if cpu.registers.V[reg1] != cpu.registers.V[reg2]:
        cpu.registers.PC += 2


def skp(cpu, reg):
    key_to_test = cpu.registers.V[reg]

    if cpu.display.pressed_keys[key_to_test]:
        cpu.registers.PC += 2


def sknp(cpu, reg):
    key_to_test = cpu.registers.V[reg]

    if not cpu.display.pressed_keys[key_to_test]:
        cpu.registers.PC += 2


def or_(cpu, reg1, reg2):
    value = cpu.registers.V[reg1] | cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def and_(cpu, reg1, reg2):
    value = cpu.registers.V[reg1] & cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def xor(cpu, reg1, reg2):
    value = cpu.registers.V[reg1] ^ cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def shr(cpu, reg1, reg2):
    cpu.registers.V[15] = cpu.registers.V[reg1] & 1

    value = cpu.registers.V[reg1] >> 1
    cpu.registers.V[reg1] = value % 256


def shl(cpu, reg1, reg2):
    if cpu.registers.V[reg1] & 128:
        cpu.registers.V[15] = 1

    value = cpu.registers.V[reg1] << 1
    cpu.registers.V[reg1] = value % 256

def rnd(cpu, reg, _and):
    cpu.registers.V[reg] = randint(0, 255) & _and
    
#########################################

instructions = {
    "cls": cls, "drw": drw, "call": call, "ret": ret, "ld1": ld1, "ld2": ld2,
    "ld3": ld3, "ld4": ld4, "ld5": ld5, "ld6": ld6, "ld7": ld7, "ld8": ld8,
    "ld9": ld9, "ld10": ld10, "ld11": ld11, "add1": add1, "add2": add2,
    "add3": add3, "sub": sub, "subn": subn, "jp1": jp1, "jp2": jp2, "se1": se1,
    "se2": se2, "sne1": sne1, "sne2": sne2, "skp": skp, "sknp": sknp, "or": or_,
    "and": and_, "xor": xor, "shr": shr, "shl": shl, "rnd": rnd
}

oper_dict = {"cls": "00e0", "drw": "dxyn", "call": "2nnn", "ret": "00ee",
             "ld1": "6xkk", "ld2": "8xy0", "ld3": "annn", "ld4": "fx07",
             "ld5": "fx0a", "ld6": "fx15", "ld7": "fx18", "ld8": "fx29",
             "ld9": "fx33", "ld10": "fx55", "ld11": "fx65", "add1": "7xkk",
             "add2": "8xy4", "add3": "fx1e", "sub": "8xy5", "subn": "8xy7",
             "jp1": "1nnn", "jp2": "bnnn", "se1": "3xkk", "se2": "5xy0",
             "sne1": "4xkk", "sne2": "9xy0", "skp": "ex9e", "sknp": "exa1",
             "or": "8xy1", "and": "8xy2", "xor": "8xy3", "shr": "8xy6",
             "shl": "8xye", "rnd": "cxkk"}

patterns = {}
for opcode, hex in oper_dict.items():
    hex_regex = (
        hex.replace("kk", "([0-9a-f]{2})")
        .replace("nnn", "([0-9a-f]{3})")
        .replace("x", "([0-9a-f])")
        .replace("y", "([0-9a-f])")
        .replace("n", "([0-9a-f])")
    )

    patterns[opcode] = hex_regex


def parse(instruction):
    instr_str = instruction.hex()
        
    for opname, hex in patterns.items():
        match = re.match(hex, instr_str)

        if not match:
            continue

        args_str = match.groups()
        args_int = [int(arg, 16) for arg in args_str]
        
        return opname, args_int

    else:
        return None

def call(cpu, instr, args):
    instructions[instr](cpu, *args)
    