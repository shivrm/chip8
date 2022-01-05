from cpu import Registers


def cls(cpu):
    cpu.display.clear()


def ld1(cpu, reg, value):
    cpu.registers.V[reg] = value


def ld2(cpu, reg1, reg2):
    cpu.registers.V[reg1] = cpu.registers.V[reg2]


def ld3(cpu, mem):
    cpu.registers.I = mem


def ld4(cpu, reg):
    cpu.registers.V[reg] = cpu.registers.DT


# TODO: Add Display APIs to allow other modules to access events
# This is necessary for ld5 as it requires waiting for keypress


def ld6(cpu, reg):
    cpu.registers.DT = cpu.registers.V[reg]


def ld7(cpu, reg):
    cpu.registers.ST = cpu.registers.V[reg]


def ld8(cpu, value):
    cpu.registers.I = value * 5


def ld9(cpu, reg):
    val = cpu.registers.V[reg]
    digits = val // 100, val // 10 % 10, val % 10

    for idx, digit in enumerate(digits):
        memloc = cpu.registers.I + idx
        cpu.memory[memloc] = digit


def ld10(cpu, reg):
    for idx in range(cpu, reg):
        memloc = cpu.registers.I + idx
        cpu.registers.V[idx] = cpu.memory[memloc]


def ld11(cpu, reg):
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


# Improved Display APIs are necessary for implementing
# skp and sknp commands


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
