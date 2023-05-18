import pathlib

def main():
    floor = 0
    with open(pathlib.Path("input.txt")) as file:
        for line in file:
            for i in range(len(line)):
                if line[i] == "(":
                    floor += 1
                elif line[i] == ")":
                    floor -= 1
                if floor == -1:
                    print(i + 1)
    print (floor)

if __name__ == "__main__":
    main()