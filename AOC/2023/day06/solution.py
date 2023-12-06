import math

with open("input.txt") as file:
    parts = file.readlines()


times = parts[0].split(':')[1].split()
times = [int(v) for v in times]

times2 = parts[0].split(':')[1].replace(" ", "").split()
times2 = [int(v) for v in times2]

dists = parts[1].split(':')[1].split()
dists = [int(v) for v in dists]

dist2 = parts[1].split(':')[1].replace(" ", "").split()
dist2 = [int(v) for v in dist2]

def answer(times, dists):
    # Hold for x secs, run for T-x secs, cover dist x*(T-x)
    # x * (Ti-x) > ci
    lower = [max(math.floor(ti/2 - math.sqrt((ti**2)/4 - ci))+1, 1) for ti,ci in zip(times, dists)]
    upper = [min(math.ceil(ti/2 + math.sqrt((ti**2)/4 - ci))-1, ti-1) for ti,ci in zip(times, dists)]

    poss = [ui - li + 1 for ui, li in zip(upper, lower)]

    prod = 1
    for v in poss:
        prod *= v

    return prod

print(answer(times, dists))

# Part 2

print(answer(times2, dist2))
