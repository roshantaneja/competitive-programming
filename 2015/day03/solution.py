import pathlib

def main():
    with open(pathlib.Path("input.txt")) as file:
        for line in file:
            for i in line:
                if i == "<":
                    print (i)