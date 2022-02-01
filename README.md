# chip8

- [chip8](#chip8)
    + [Installation](#installation)
    + [Global Installation](#global-installation)
    + [Add it to a specific project](#add-it-to-a-specific-project)
    + [Uninstall](#uninstall)
  * [Usage](#usage)
    + [Command Line Usage](#command-line-usage)
    + [Using in Python scripts](#using-in-python-scripts)
  * [ROMs](#roms)
  * [License](#license)

---

An emulator for the CHIP-8 programming language, written in Python. Supports almost all major CHIP-8 instructions.

The CHIP-8 virtual machine can be either imported as a module in Python scripts, or run from the command line.

### Installation
You can install the emulator either globally, or add it to a specific project.

First, clone the git repository, or download the source code.

### Global Installation
 - Navigate to the project folder
 - Run `pip install .` from the command line

### Add it to a specific project
 - Navigate to the project folder
 - Copy the `chip8` folder to your project folder.

### Uninstall
 - To uninstall a global installation, run `pip uninstall chip8` from the command-line
 - To remove `chip8` from a specific project, just delete the folder.

## Usage
Once installed, the emulator can be run from the command line using `python -m chip8 [arguments]`. You can also use it in Python files using `import chip8`

### Command Line Usage
`python -m chip8 <file> [-h] [--url] [--speed SPEED] [--fgcolor FGCOLOR [FGCOLOR ...]] [--bgcolor BGCOLOR [BGCOLOR ...]] [--keys KEYS] [--scale SCALE]`

 - `--help` `-h`: Provides help about the command

 - `file`: A path to the CHIP-8 ROM
 - `--url` `-u`:  If this flag is present, the file path is assumed to be a 	URL (`False` by default) 
 - `--speed` `-s`:  A number specifying how many CPU cycles should be run per second (`60`Hz by default)
 -  `--fgcolor` `-fg`: Three integers representing RGB value of foreground color (`255 255 255` by default)
 -  `--bgcolor` `-bg`: Three integers representing RGB value of background color (`0 0 0` by default)
 -  `--keys` `-k`: A string of 16 characters. The key for each character will be used as keys `0` through `f` of the CHIP-8 keyboard (`X123QWEASDZC4RFV` by default)
 - `--scale` `-x`: The factor by which the display should be scaleed (`10`x by default)

Example: 
```
python -m chip8 https://url.to/file -u --speed 100 --fgcolor 255 0 0 -x 20
```

### Using in Python scripts
The package can be imported using `import chip8`. It contains the `CPU` and `Display` classes, and the `instr` module

#### `CPU`
The `CPU` class defines a fully functional CHIP-8 CPU. This can be used to run a CHIP-8 ROM. The constructor accepts all the agruments described in the above section.

The example above - `python -m chip8 https://url.to/file -u --speed 100 --fgcolor 255 0 0 -x 20
` can be written using `chip8.CPU` as:
```py
import chip8
chip8.CPU(file="https://url.to/file", speed=100, fgcolor=(255, 0, 0), scale=20)
```

#### `Display`
The `Display` class provides a pygame display, and is also used to figure out which keys are pressed.

It can be used as follows:
```py
import chip8

display = chip8.Display(
	fgcolor=(255, 255, 255), # Foreground color (R G and B values)
	bgcolor=(0, 0, 0), # Background color (R G and B values)
	keys="X123QWEASDZC4RFV", # Keys corresponding to 0 through F on CHIP-8 keyboard
	scale=10 # Factor to scale the display by
)

display.set_color(
	(255, 0, 0), # Background color
	(0, 0, 255), # Backfround color
	clear=True   # Clears the display after changing color
)

display.update() # Update the display and handles events

print(display.pressed_keys) # A boolean list of 16 elements used to show which keys are pressed

display.set_keys("7890UIOPJKL;M,./") # Change the keys

display.quit() # Stop the display
```

#### `instr`
The `instr` submodule contains the instruction set, and parser for the emulator. The `parse` function accepts a `bytearray` of length 2, and returns the operation name, and arguments.

The `call` function accepts a `CPU` object, an operation name, and a list of arguments. It then calls the function associated with the operation name, with the correct arguments.

## ROMs
Here are a few popular CHIP-8 ROM collections:
 - [kripod/chip8-roms: ROMs for CHIP-8. (github.com)](https://github.com/kripod/chip8-roms)
 - [chip8Archive - A collection of public domain (CC0) games, all playable online](https://johnearnest.github.io/chip8Archive/)
 - [mattmikolay/chip-8: A collection of CHIP-8 programs and documentation (github.com)](https://github.com/mattmikolay/chip-8)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE)

Copyright &copy; shivrm 2022

[Back to top](#chip8)