class Registers:
    V = bytearray(16)
    I = 0x00

    PC = 0x00
    SP = 0x00

class CPU(object):
    def __init__(self) -> None:
        
        self.memory = bytearray(16 ** 3)
        self.registers = Registers()