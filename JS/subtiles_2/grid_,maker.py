# make a 13x13 grid of "__" with spaces in between

size = 5
row = " ".join(["__"] * size)

for _ in range(size):
    print(row)