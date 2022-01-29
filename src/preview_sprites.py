# Open file and read the bytes
with open("./src/sprites", "rb") as f:
    binary = list(f.read(80))

# Convert the list of bytes to a list of binary strings containing
# only the first 4 bits of the 8-bit binary representation
bin_strs = [bin(b)[2:-4] for b in binary]

# Then split the list into groups of 5, containing each sprite
sprites = [bin_strs[idx : idx + 5] for idx in range(0, 80, 5)]

# Pad the binary representation, then replace the 0s and 1s with
# spaces and blocks respectively. After this, print the sprite
for sprite in sprites:
    for line in sprite:
        padded = line.zfill(4)
        formatted = padded.replace("0", "  ").replace("1", "██")

        print(formatted)

    print()
