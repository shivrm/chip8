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
        self.stack = [0] * 16
        self.registers = Registers()

        # Laod rom and initialize display
        self.load_rom(rom)
        self.display = Display()

        # Load sprites and start event loop
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

            # If instruction is 0x00 0x00, then wait for input, then end loop
            if instr.hex() == "0000":
                input("Program end")
                self.display.quit()
                return

            # Reduce value of DT, if nonzero, on each cycle
            if self.registers.DT:
                self.registers.DT -= 1

            self.handle(instr)  # Handle the instruction

            self.registers.PC += 2  # Increment the program counter

    def handle(self, opcode):
        # Parse the instruction
        opname, args = instr.parse(opcode)

        # Used for debugging
        # v_data = " ".join(["{:02x}".format(x) for x in self.registers.V])
        # print(f"{hex(self.registers.PC)} | {opcode.hex()} ({opname}); V: {v_data}, I: {self.registers.I}")

        # Invoke the instruction
        instr.call(self, opname, args)

    def load_rom(self, rom_loc):
        """Loads a ROM into memory

        Args:
            rom_loc (string): File path of the rom
        """
        with open(rom_loc, "rb") as f:
            data = f.read()

        # Write into memory starting at 0x200
        for idx, byte in enumerate(data):
            self.memory[0x200 + idx] = byte


CPU("test/test_opcode.ch8")
