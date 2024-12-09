import re

with open("input.txt") as file:
    lines = file.readlines()

total = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    target, nums = line.split(":")
    target = int(target.strip())
    arr = list(map(int, nums.strip().split()))
    dp = {arr[0]}
    for x in arr[1:]:
        new_dp = set()
        for val in dp:
            new_dp.add(val + x)
            new_dp.add(val * x)
        dp = new_dp
    if target in dp:
        total += target

print(total)


def apply_operator(val1, val2, operator):
    if operator == '+':
        return val1 + val2
    elif operator == '*':
        return val1 * val2
    elif operator == '||':
        return int(f"{val1}{val2}")

total = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    target, nums = line.split(":")
    target = int(target.strip())
    arr = list(map(int, nums.strip().split()))
    dp = {arr[0]}
    
    for x in arr[1:]:
        new_dp = set()
        for val in dp:
            new_dp.add(val + x)          # Addition
            new_dp.add(val * x)          # Multiplication
            new_dp.add(apply_operator(val, x, '||'))  # Concatenation
        dp = new_dp
    
    if target in dp:
        total += target

print(total)