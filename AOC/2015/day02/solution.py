import pathlib

def main():
    total = 0
    ribbon = 0
    with open(pathlib.Path("input.txt")) as file:
        for line in file:
            a = int(line.split("x")[0])
            b = int(line.split("x")[1])
            c = int(line.split("x")[2])
            total += (2 * a * b + 2 * b * c + 2 * c * a + min(a * b, b * c,
                                                            c * a))
            ribbon += (2 * min(a + b, b + c, c + a) + a * b * c)
    print(total)
    print(ribbon)

if __name__ == "__main__":
    main()