import re
with open('input.txt', 'r') as file:
    lines = file.readlines()

left_list = []
right_list = []

for line in lines:
    left, right = map(int, line.split())
    left_list.append(left)
    right_list.append(right)

left_list.sort()
right_list.sort()

total_distance = sum(abs(l - r) for l, r in zip(left_list, right_list))

print("Total Distance:", total_distance)

right_counter = {}
for num in right_list:
    if num in right_counter:
        right_counter[num] += 1
    else:
        right_counter[num] = 1

similarity_score = 0
for num in left_list:
    if num in right_counter:
        similarity_score += num * right_counter[num]

print("Similarity Score:", similarity_score)