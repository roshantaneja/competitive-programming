import re

with open('input.txt', 'r') as file:

    lines = [list(line.rstrip('\n')) for line in file.readlines()]

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}
direction_keys = ['^', '>', 'v', '<']

rows = len(lines)
cols = len(lines[0])

start_r, start_c, start_d = None, None, None
for r in range(rows):
    for c in range(cols):
        if lines[r][c] in directions:
            start_r, start_c = r, c
            start_d = lines[r][c]
            break
    if start_r is not None:
        break

visited = set()
visited.add((start_r, start_c))

d_index = direction_keys.index(start_d)

def turn_right(d_idx):
    return (d_idx + 1) % 4

r, c = start_r, start_c

while True:
    dr, dc = directions[direction_keys[d_index]]
    front_r, front_c = r + dr, c + dc

    if 0 <= front_r < rows and 0 <= front_c < cols:
        if lines[front_r][front_c] == '#':
            d_index = turn_right(d_index)
        else:
            r, c = front_r, front_c
            visited.add((r, c))
    else:
        break

print(len(visited))





with open('input.txt', 'r') as file:
    original_lines = [list(line.rstrip('\n')) for line in file.readlines()]

directions = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}
direction_keys = ['^', '>', 'v', '<']

rows = len(original_lines)
cols = len(original_lines[0])

start_r, start_c, start_d = None, None, None
for r in range(rows):
    for c in range(cols):
        if original_lines[r][c] in directions:
            start_r, start_c = r, c
            start_d = original_lines[r][c]
            break
    if start_r is not None:
        break

def turn_right(d_idx):
    return (d_idx + 1) % 4

def simulate(lines):
    visited_states = set()
    d_index = direction_keys.index(start_d)
    r, c = start_r, start_c
    visited_states.add((r, c, d_index))
    while True:
        dr, dc = directions[direction_keys[d_index]]
        front_r, front_c = r + dr, c + dc

        if 0 <= front_r < rows and 0 <= front_c < cols:
            if lines[front_r][front_c] == '#':
                d_index = turn_right(d_index)
            else:
                r, c = front_r, front_c
                state = (r, c, d_index)
                if state in visited_states:
                    return True  # loop detected
                visited_states.add(state)
        else:
            return False  # guard leaves the area

count = 0
for rr in range(rows):
    for cc in range(cols):
        if (rr, cc) != (start_r, start_c):
            if original_lines[rr][cc] == '.':
                lines = [row[:] for row in original_lines]
                lines[rr][cc] = '#'
                if simulate(lines):
                    count += 1

print(count)