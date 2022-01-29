import re
import toml
from random import randint


def cls(cpu):
    """Clears the display"""
    cpu.display.clear()


def drw(cpu, reg_x, reg_y, num_bytes):
    """Draws a sprite num_bytes long, at reg_x, reg_y"""
    x_start = cpu.registers.V[reg_x]
    y_start = cpu.registers.V[reg_y]

    for byte_idx in range(num_bytes):
        row = (y_start + byte_idx) % 32  # Calculate row
        sprite_val = cpu.memory[cpu.registers.I + byte_idx]

        for col_offset in range(8):
            # Get col_offset-th bit from the left
            set_bit = sprite_val & (128 >> col_offset)
            col = (x_start + col_offset) % 64  # Calculate column

            if set_bit:
                # Set VF if pixel was unset
                cpu.registers.V[15] = cpu.display.flip(col, row) or cpu.registers.V[15]


def call(cpu, mem_addr):
    """Calls a subroutine

    Args:
        mem_addr (int12): The memory address of the subroutine to call
    """

    # Ensure that stack size does not exceed 16
    if cpu.registers.SP == 15:
        raise IndexError("Stack Overflow: Stack size exceeds 16")

    # Push the current memory location onto the stack
    cpu.stack[cpu.registers.SP] = cpu.registers.PC
    cpu.registers.SP += 1

    # Set the program counter to the new location
    # Subtract 2 to account for increment by CPU
    cpu.registers.PC = mem_addr - 2


def ret(cpu):
    """Returns from a subroutine back to the parent process"""

    # Ensure that the stack is not empty
    if cpu.registers.SP == 0:
        raise IndexError("Stack Underflow: Stack is empty")

    # Pop the topmost value and store it in the program counter
    # Don't subract 2, so that call instruction is skipped
    cpu.registers.SP -= 1
    cpu.registers.PC = cpu.stack[cpu.registers.SP]


def ld1(cpu, register, value):
    """Loads a constant value into a register"""
    cpu.registers.V[register] = value


def ld2(cpu, reg_to, reg_from):
    """Loads the value of one register into another"""
    cpu.registers.V[reg_to] = cpu.registers.V[reg_from]


def ld3(cpu, value):
    """Loads a 12 bit value into the I register"""
    cpu.registers.I = value


def ld4(cpu, register):
    """Loads the value of DT into a register"""
    cpu.registers.V[register] = cpu.registers.DT


def ld5(cpu, register):
    """Loads the value of the pressed key into a register.
    Waits until a key is pressed
    """

    # While no keys are pressed, keep returning to this instruction
    if not any(cpu.display.pressed_keys):
        cpu.registers.PC -= 2
        return

    # Set the register to the first pressed key in the list
    cpu.registers.V[register] = cpu.display.pressed_keys.index(True)


def ld6(cpu, register):
    """Loads the value of a register into DT"""
    cpu.registers.DT = cpu.registers.V[register]


def ld7(cpu, register):
    """Loads the value of a register into ST"""
    cpu.registers.ST = cpu.registers.V[register]


def ld8(cpu, reg):
    """Set the I register to the memory location where the sprite
    for the digit corresponding to unit digit of reg is stored
    """

    # Since the sprites are stored starting at memory address 0,
    # And each sprite occupies 5 bytes, we can obtain the location
    # of the sprite by multiplying the corresponding digit by 5
    digit = cpu.registers.V[reg] % 16
    cpu.registers.I = digit * 5


def ld9(cpu, register):
    """Loads the BCD representation of the value in a register into
    the memory addresses at I, I+1 and I+2
    """

    # Split the value of the register into hundreds, tens ,and units
    val = cpu.registers.V[register]
    digits = val // 100, val // 10 % 10, val % 10

    # Store the digits at memory addresses I, I+1 and I+2
    for idx, digit in enumerate(digits):
        memloc = cpu.registers.I + idx
        cpu.memory[memloc] = digit


def ld10(cpu, register):
    """Sets the value at memory locations I through I + (register - 1) from
    registers V0 through V(register - 1)
    """

    # Loop with idx = 0 through reg - 1. Get the memory address and store
    # the value of each register at the memory addresses
    for idx in range(register + 1):
        memloc = cpu.registers.I + idx
        cpu.memory[memloc] = cpu.registers.V[idx]


def ld11(cpu, register):
    """Loads registers V0 through V(register - 1) with the values in memory from
    I to I + (register - 1)
    """

    # Loop with idx = 0 through reg - 1. Get the memory address and load
    # the register with the value at that address
    for idx in range(register + 1):
        memloc = cpu.registers.I + idx
        cpu.registers.V[idx] = cpu.memory[memloc]


def add1(cpu, register, value):
    """Adds a constant value to a register"""
    added = cpu.registers.V[register] + value
    cpu.registers.V[register] = added % 256


def add2(cpu, reg_to, reg_from):
    """Adds the value of one register into another"""

    # Add the two values and set VF if there is an overflow
    added = cpu.registers.V[reg_to] + cpu.registers.V[reg_from]
    cpu.registers.V[15] = added > 255

    # Load the value, mod 256, into reg_to
    cpu.registers.V[reg_to] = added % 256


def add3(cpu, register):
    """Adds the value of a register into the I register"""

    # Add the values, and load it into the I register, mod 65536
    added = cpu.registers.I + cpu.registers.V[register]
    cpu.registers.I = added % 65536


def sub(cpu, reg1, reg2):
    """Subtracts the value in reg2 from the value in reg1, and store it in reg1
    VF is set if carry does not occur"""
    subbed = cpu.registers.V[reg1] - cpu.registers.V[reg2]
    cpu.registers.V[15] = subbed >= 0
    cpu.registers.V[reg1] = subbed % 256


def subn(cpu, reg1, reg2):
    """Subtracts the value in reg1 from the value in reg2, and store it in reg1
    VF is set if carry does not occur"""
    subbed = cpu.registers.V[reg2] - cpu.registers.V[reg1]
    cpu.registers.V[15] = subbed >= 0
    cpu.registers.V[reg2] = subbed % 256


def jp1(cpu, mem):
    """Jump to memory address mem"""
    # Subtract 2 to account for increment by CPU
    cpu.registers.PC = mem - 2


def jp2(cpu, mem):
    """Jump to memory address mem + value in V[0]"""
    # Subtract 2 to account for increment by CPU
    cpu.registers.PC = mem + cpu.registers.V[0] - 2


def se1(cpu, reg, value):
    """Skip next instruction if value in reg equals value"""
    if cpu.registers.V[reg] == value:
        cpu.registers.PC += 2


def se2(cpu, reg1, reg2):
    """Skip the next instruction if value in reg1 equals value in reg2"""
    if cpu.registers.V[reg1] == cpu.registers.V[reg2]:
        cpu.registers.PC += 2


def sne1(cpu, reg, value):
    """Skip next instruction if value in reg does not equal value"""
    if cpu.registers.V[reg] != value:
        cpu.registers.PC += 2


def sne2(cpu, reg1, reg2):
    """Skip next instruction if value in reg1 does not equal value in reg2"""
    if cpu.registers.V[reg1] != cpu.registers.V[reg2]:
        cpu.registers.PC += 2


def skp(cpu, reg):
    """Skip next instruction if key with value of unit digit of reg is pressed"""
    key_to_test = cpu.registers.V[reg] % 16

    if cpu.display.pressed_keys[key_to_test]:
        cpu.registers.PC += 2


def sknp(cpu, reg):
    """Skip next instruction if key with value of unit digit of reg is not pressed"""
    key_to_test = cpu.registers.V[reg] % 16

    if not cpu.display.pressed_keys[key_to_test]:
        cpu.registers.PC += 2


def or_(cpu, reg1, reg2):
    """Perform a bitwise or between values in reg1 and reg2 and store in reg1"""
    value = cpu.registers.V[reg1] | cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def and_(cpu, reg1, reg2):
    """Perform a bitwise and between values in reg1 and reg2 and store in reg1"""
    value = cpu.registers.V[reg1] & cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def xor(cpu, reg1, reg2):
    """Perform a bitwise xor between values in reg1 and reg2 and store in reg1"""
    value = cpu.registers.V[reg1] ^ cpu.registers.V[reg2]
    cpu.registers.V[reg1] = value


def shr(cpu, reg1, reg2):
    """Shift value in reg1 to right, VF is set if lowest bit was set"""
    cpu.registers.V[15] = cpu.registers.V[reg1] & 1

    value = cpu.registers.V[reg1] >> 1
    cpu.registers.V[reg1] = value % 256


def shl(cpu, reg1, reg2):
    """Shift value in reg1 to left, VF is set if highest bit was set"""
    if cpu.registers.V[reg1] & 128:
        cpu.registers.V[15] = 1

    value = cpu.registers.V[reg1] << 1
    cpu.registers.V[reg1] = value % 256


def rnd(cpu, reg, _and):
    """Sets the value of reg to a random number between 0 and 255,
    bitwise-ANDed with _and"""
    cpu.registers.V[reg] = randint(0, 255) & _and


#########################################

# List of instructions
instructions = {
    "cls": cls,
    "drw": drw,
    "call": call,
    "ret": ret,
    "ld1": ld1,
    "ld2": ld2,
    "ld3": ld3,
    "ld4": ld4,
    "ld5": ld5,
    "ld6": ld6,
    "ld7": ld7,
    "ld8": ld8,
    "ld9": ld9,
    "ld10": ld10,
    "ld11": ld11,
    "add1": add1,
    "add2": add2,
    "add3": add3,
    "sub": sub,
    "subn": subn,
    "jp1": jp1,
    "jp2": jp2,
    "se1": se1,
    "se2": se2,
    "sne1": sne1,
    "sne2": sne2,
    "skp": skp,
    "sknp": sknp,
    "or": or_,
    "and": and_,
    "xor": xor,
    "shr": shr,
    "shl": shl,
    "rnd": rnd,
}

# Load instrucion hex format
with open("./src/instr.toml", "r") as f:
    oper_dict = toml.load(f)

# Create list of regex patterns to match instructions
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
    """Parses an instruction given it's hex-code (bytearray of length 2)
    Returns the operation name, and a list of arguments
    """
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
    """Calls the function associated with an operation name"""
    instructions[instr](cpu, *args)
