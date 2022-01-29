from bdb import Breakpoint
from display import Display
import instr
from time import sleep

class Registers:
    V = bytearray(16)
    I = 0x00

    PC = 0x200
    SP = 0x00

    ST = 0x00
    DT = 0x00


class CPU(object):
    def __init__(self, rom) -> None:
        # Initialize the memory, stack and registers
        self.memory = bytearray(16 ** 3)
        self.stack = bytearray(16)
        self.registers = Registers()

        self.load_rom(rom)
        self.display = Display()

        self.load_sprites()
        self.loop()

    def load_sprites(self):
        # Open the file containing the sprites and read the bytes
        with open("./src/sprites", "rb") as f:
            binary = list(f.read(80))

        # Write the bytes to memory, from 0x000 to 0x07f
        for idx, b in enumerate(binary):
            self.memory[idx] = b

    def loop(self):
        while True:
            self.display.update()  # Handle display events

            # Get the instruction from memory
            instr = self.memory[self.registers.PC : self.registers.PC + 2]

            if instr.hex() == "0000":
                self.display.quit()
                Breakpoint

            self.handle(instr)  # Handle the instruction

            sleep(0.01)
            self.registers.PC += 2  # Increment the program counter

    def handle(self, opcode):
        opname, args = instr.parse(opcode)

        instr.call(self, opname, args)
        
    def load_rom(self, rom_loc):
        with open(rom_loc, "rb") as f:
            data = f.read()
            
        for idx, byte in enumerate(data):
            self.memory[0x200 + idx] = byte
            
CPU("test/divtest.ch8")