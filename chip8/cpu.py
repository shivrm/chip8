from .display import Display
from . import instr

import urllib.request
from time import sleep


class Registers:
    V = bytearray(16)
    I = 0x00

    PC = 0x200  # Program counter
    SP = 0x00  # Stack pointer

    # Sound and display timers
    ST = 0x00
    DT = 0x00


class CPU(object):
    def __init__(
        self,
        file,
        fgcolor=(255, 255, 255),
        bgcolor=(0, 0, 0),
        keys="X123QWEASDZC4RFV",
        speed=60,
        scale=10,
        url=False,
    ) -> None:
        # Initialize the memory, stack and registers
        self.memory = bytearray(16 ** 3)
        self.stack = [0] * 16
        self.registers = Registers()

        self.sleep_time = 1 / speed

        self.load_rom(file, url)
        self.display = Display(fgcolor, bgcolor, keys, scale)

        # Load sprites and start event loop
        self.load_sprites()
        self.loop()

    def load_sprites(self):
        # Binary data for the sprites
        sprites = (b'\xf0\x90\x90\x90\xf0 `  p\xf0\x10\xf0\x80\xf0\xf0\x10\xf0'
                   b'\x10\xf0\x90\x90\xf0\x10\x10\xf0\x80\xf0\x10\xf0\xf0\x80'
                   b'\xf0\x90\xf0\xf0\x10 @@\xf0\x90\xf0\x90\xf0\xf0\x90\xf0'
                   b'\x10\xf0\xf0\x90\xf0\x90\x90\xe0\x90\xe0\x90\xe0\xf0\x80'
                   b'\x80\x80\xf0\xe0\x90\x90\x90\xe0\xf0\x80\xf0\x80\xf0\xf0'
                   b'\x80\xf0\x80\x80')

        # Write the bytes to memory, from 0x000 to 0x07f
        for idx, b in enumerate(sprites):
            self.memory[idx] = b

    def loop(self):
        while True:

            # Try to update display - raises error if display has been quit
            try:
                self.display.update()  # Handle display events
            except:
                return

            # Get the instruction from memory
            instr = self.memory[self.registers.PC : self.registers.PC + 2]

            # Stop execution if instruction is 0x00 0x00
            if instr.hex() == "0000":
                self.display.quit()
                return

            # Decrement the delay timer if it is nonzero
            if self.registers.DT:
                self.registers.DT -= 1

            self.handle(instr)  # Handle the instruction

            sleep(self.sleep_time)
            self.registers.PC += 2  # Increment the program counter

    def handle(self, opcode):
        """Handles the instruction

        Args:
            opcode (bytearray[2]): A bytearray of length 2, containing
            the bytes for the instruction opcode
        """

        # Parse the instruction into operation name and arguments
        opname, args = instr.parse(opcode)

        # For debug
        # v_data = " ".join(["{:02x}".format(x) for x in self.registers.V])
        # print(f"{hex(self.registers.PC)} | {opcode.hex()} ({opname}); V: {v_data}, I: {self.registers.I}")

        # Call the function associated with the instruction
        instr.call(self, opname, args)

    def load_rom(self, rom_loc, url):

        # Open ROM and read data
        if not url:
            with open(rom_loc, "rb") as f:
                data = f.read()

        else:
            data = urllib.request.urlopen(rom_loc).read()

        # Write to memory starting at 0x200
        for idx, byte in enumerate(data):
            self.memory[0x200 + idx] = byte
