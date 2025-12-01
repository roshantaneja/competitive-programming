import re
with open('input.txt', 'r') as file:
    lines = file.readlines()

pos = 50

count_end = 0
count_all = 0

for line in lines:
    line = line.strip()
    if not line:
        continue

    direction = line[0].upper()
    dist = int(line[1:])

    start = pos

    if direction == 'L':
        first_k = start % 100
        if first_k == 0:
            first_k = 100
        if first_k <= dist:
            count_all += 1 + (dist - first_k) // 100

        pos = (pos - dist) % 100
    else:
        first_k = (100 - start) % 100
        if first_k == 0:
            first_k = 100
        if first_k <= dist:
            count_all += 1 + (dist - first_k) // 100

        pos = (pos + dist) % 100

    if pos == 0:
        count_end += 1

print(count_end)
print(count_all)