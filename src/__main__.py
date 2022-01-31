import argparse
from .cpu import CPU

parser = argparse.ArgumentParser(description="An interpreter for CHIP-8 programs")

parser.add_argument("file", help="path to a CHIP-8 ROM")
parser.add_argument("--speed", "-s", type=int, help="aumber of cycles to execute per second")

parser.add_argument("--fgcolor", "-fg", type=int, nargs='+', help="a 3-tuple containing RGB values for foreground color")
parser.add_argument("--bgcolor", "-bg", type=int, nargs='+', help="a 3-tuple containing RGB values for background color")

parser.add_argument("--keys", "-k", type=str, help="a string of 16 characters to be used as the keys.")

args = parser.parse_args()

try:
    open(args.file)
except:
    raise argparse.ArgumentTypeError("file could not be opened")

if args.fgcolor and len(args.fgcolor) != 3:
    raise argparse.ArgumentTypeError("--fgcolor is invalid")

if args.bgcolor and len(args.bgcolor) != 3:
    raise argparse.ArgumentTypeError("--bgcolor is invalid")

if args.keys and len(args.keys) != 16:
        raise argparse.ArgumentTypeError("--keys is invalid")

args_dict = {k:v for k, v in args.__dict__.items() if v is not None}

cpu = CPU(**args_dict)