class Registers:
    V = bytearray(16)
    I = 0x00

    VF = 0x00

    PC = 0x00
    SP = 0x00

    ST = 0x00
    DT = 0x00


class CPU(object):
    def __init__(self) -> None:

        self.memory = bytearray(16 ** 3)
        self.stack = bytearray(16)
        self.registers = Registers()

    def load_sprites(self):
        with open("./src/sprites", "rb") as f:
            binary = list(f.read(80))

        for idx, b in enumerate(binary):
            self.memory[idx] = b
