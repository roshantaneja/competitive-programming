import pathlib


offset = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}

content = []
with open(pathlib.Path("input.txt")) as file:
    for line in file:
        content.append(line)



# do NOT ask why i wrote this, im not gonna answer you
def parse(i):
    a, b = content[i].split()
    yield a, int(b)

#part 1
headx, heady = 0, 0
tailx,taily = 0, 0
seen = {(0, 0)}

for i in range(len(content)):
    for d, n in parse(i):
        dx, dy = offset[d]
        for _ in range(n):
            headx += dx
            heady += dy
            while max(abs(tailx - headx), abs(taily - heady)) > 1:
                if abs(tailx - headx) > 0:
                    tailx += 1 if headx > tailx else -1
                if abs(taily - heady) > 0:
                    taily += 1 if heady > taily else -1
                seen.add((tailx, taily))

print(len(seen))

# part 2 (courtesy of theodore)
rope = [(0, 0)] * 10
headx, heady = 0, 0
tailx,taily = 0, 0
seen = set()
for i in range(len(content)):
    for d, n in parse(i):
        dx, dy = offset[d]
        for _ in range(n):
            headx, heady = rope[0]
            rope[0] = headx + dx, heady + dy

            for i in range(1, len(rope)):
                px, py = rope[i-1]
                kx, ky = rope[i]
                while max(abs(kx - px), abs(ky - py)) > 1:
                    if abs(kx - px) > 0:
                        kx += 1 if px > kx else -1
                    if abs(ky - py) > 0:
                        ky += 1 if py > ky else -1
                rope[i] = kx, ky

            seen.add(rope[-1])

print(len(seen))

# only possile becus of teho