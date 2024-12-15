with open("input.txt") as file:
    raw = file.read().strip('\n')

lines = raw.split('\n')

# Identify map lines
map_lines = []
i = 0
while i < len(lines) and lines[i].strip():
    line_check = lines[i]
    if not all(ch in '#.O@' for ch in line_check.strip()):
        break
    map_lines.append(line_check)
    i += 1

move_lines = lines[i:]
moves_str = "".join(move_lines).replace('\n','').strip()

directions = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}



###########################
# PART 1 IMPLEMENTATION
###########################
warehouse = [list(row) for row in map_lines]
rows = len(warehouse)
cols = len(warehouse[0]) if rows > 0 else 0

robot_x = robot_y = None
for y in range(rows):
    for x in range(cols):
        if warehouse[y][x] == '@':
            robot_x, robot_y = x, y
            break
    if robot_x is not None:
        break

def can_push(wh, x, y, dx, dy):
    # Find chain of boxes in the direction (dx,dy)
    chain = []
    cx, cy = x, y
    while 0 <= cy < len(wh) and 0 <= cx < len(wh[0]) and wh[cy][cx] == 'O':
        chain.append((cx, cy))
        cx += dx
        cy += dy
    # The next cell must be '.' to push
    if not (0 <= cy < len(wh) and 0 <= cx < len(wh[0])):
        return False
    if wh[cy][cx] != '.':
        return False
    return True

def do_push(wh, x, y, dx, dy):
    chain = []
    cx, cy = x, y
    while 0 <= cy < len(wh) and 0 <= cx < len(wh[0]) and wh[cy][cx] == 'O':
        chain.append((cx, cy))
        cx += dx
        cy += dy
    # Push from end
    for bx, by in reversed(chain):
        wh[by+dy][bx+dx] = 'O'
        wh[by][bx] = '.'

def move_robot(wh, rx, ry, dx, dy):
    nx, ny = rx+dx, ry+dy
    if wh[ny][nx] == '#':
        return rx, ry
    elif wh[ny][nx] == '.':
        wh[ry][rx], wh[ny][nx] = '.', '@'
        return nx, ny
    elif wh[ny][nx] == 'O':
        if can_push(wh, nx, ny, dx, dy):
            do_push(wh, nx, ny, dx, dy)
            wh[ry][rx], wh[ny][nx] = '.', '@'
            return nx, ny
        else:
            return rx, ry
    else:
        # Unexpected character, just no move
        return rx, ry

def part1(warehouse, robot_x, robot_y, moves_str):
    for m in moves_str:
        dx, dy = directions[m]
        robot_x, robot_y = move_robot(warehouse, robot_x, robot_y, dx, dy)
    total = 0
    for y in range(rows):
        for x in range(cols):
            if warehouse[y][x] == 'O':
                total += 100*y + x
    return total

# Save original warehouse and robot pos for part 2
original_warehouse = [row[:] for row in warehouse]
original_robot_x, original_robot_y = robot_x, robot_y

answer_part1 = part1(warehouse, robot_x, robot_y, moves_str)
print("Part 1:", answer_part1)



import sys

with open("input.txt") as file:
    raw = file.read().strip('\n')

lines = raw.split('\n')

# Identify map lines
map_lines = []
i = 0
while i < len(lines) and lines[i].strip():
    line_check = lines[i]
    if not all(ch in '#.O@' for ch in line_check.strip()):
        break
    map_lines.append(line_check)
    i += 1

move_lines = lines[i:]
moves_str = "".join(move_lines).replace('\n','').strip()
