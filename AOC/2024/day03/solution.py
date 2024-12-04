import re

with open('input.txt', 'r') as file:
    lines = file.readlines()

corrupted_memory = ''.join(lines)

pattern = r"mul\((\d+),(\d+)\)"

matches = re.findall(pattern, corrupted_memory)

total = 0
for match in matches:
    x, y = map(int, match)
    total += x * y
print(total)


pattern = r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)"

instructions = re.finditer(pattern, corrupted_memory)

total = 0
mul_enabled = True

for match in instructions:
    if match.group(1) and match.group(2):
        if mul_enabled:
            x, y = int(match.group(1)), int(match.group(2))
            total += x * y
    elif match.group(0) == "do()":
        mul_enabled = True
    elif match.group(0) == "don't()":
        mul_enabled = False

print(total)