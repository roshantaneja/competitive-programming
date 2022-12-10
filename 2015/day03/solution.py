import pathlib


offset = {"<": (-1, 0), ">": (1, 0), "^": (0, 1), "V": (0, -1)}

seen = {(0, 0)}
def main():
    with open(pathlib.Path("input.txt")) as file:
        for line in file:
            for i in line:
                dx, dy = offset[i]:
