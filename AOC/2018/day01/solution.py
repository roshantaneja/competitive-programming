import itertools
data = [int(x) for x in open("input.txt").readlines()]
print(sum(data))

freq = 0
seen = {0}
for num in data:
    freq += num
    if freq in seen:
        print(freq); break
    seen.add(freq)

