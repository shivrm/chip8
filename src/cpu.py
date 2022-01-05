from display import Display


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

        # Initialize the memory, stack and registers
        self.memory = bytearray(16 ** 3)
        self.stack = bytearray(16)
        self.registers = Registers()

        self.display = Display()

        self.load_sprites()

    def load_sprites(self):
        # Open the file containing the sprites and read the bytes
        with open("./src/sprites", "rb") as f:
            binary = list(f.read(80))

        # Write the bytes to memory, from 0x000 to 0x07f
        for idx, b in enumerate(binary):
            self.memory[idx] = b

    def loop(self):
        self.display.update()  # Handle display events

        # Get the instruction from memory
        instr = self.memory[self.registers.PC : self.registers.PC + 1]
        self.handle(instr)  # Handle the instruction

        self.registers.PC += 1  # Increment the program counter

    def handle(instr):
        # NotImplemented
        pass
