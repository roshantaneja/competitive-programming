import math
import re
from collections import defaultdict

with open("input.txt") as f:
    ls = f.read().strip().split("\n")

good_ids = 0
total_power = 0
for l in ls:
    parts = re.sub("[;,:]", "", l).split()
    counts = map(int, parts[2::2])
    colors = parts[3::2]
    colormax = defaultdict(int)
    for count, color in zip(counts, colors):
        colormax[color] = max(colormax[color], count)
    power = math.prod(colormax[c] for c in ("red", "green", "blue"))
    if colormax["red"] <= 12 and colormax["green"] <= 13 and colormax["blue"] <= 14:
        good_ids += int(parts[1])
    total_power += power

# Part 1
print(good_ids)

# Part 2
print(total_power)
