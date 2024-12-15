raw = open('input.txt').read().strip('\n')

lines = raw.split('\n')

# Identify where the map ends. The map consists of lines with '#', '.', 'O', '@'.
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

# Directions dictionary
directions = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}

# PART 1 LOGIC (as previously defined):
#
# If needed for part 1, we can run the simulation on the original warehouse.
# However, the user last requested code related to the final snippet,
# which handles scaled maps and pushing boxes represented as '[', ']'.
#
# For completeness, let's include the scaling logic as well.
# If you do not need part 1 anymore, you can omit it.

def scale_up_map(original_wh):
    """
    Scale the map horizontally:
    # -> ##
    O -> []
    . -> ..
    @ -> @.
    """
    mapping = {
        '#': "##",
        'O': "[]",
        '.': "..",
        '@': "@."
    }
    scaled = []
    for row in original_wh:
        new_line = "".join(mapping[ch] for ch in row)
        scaled.append(list(new_line))
    return scaled

# For part 2, we need the scaled-up warehouse.
scaled_warehouse = scale_up_map(map_lines)
scaled_rows = len(scaled_warehouse)
scaled_cols = len(scaled_warehouse[0]) if scaled_rows > 0 else 0

# Convert moves_str into a list of direction tuples
moves = [directions[m] for m in moves_str if m in directions]

def addt(x, y):
    # Add tuples element-wise
    return (x[0] + y[0], x[1] + y[1])

# Convert the scaled warehouse into walls, boxes, and robot position sets
walls = set()
boxes = set()
robot = None

# Parse the scaled warehouse:
# Each cell is a single character now. Boxes are represented as '[' at position (i,j) and ']' at (i,j+1).
for i, line in enumerate(scaled_warehouse):
    for j, ch in enumerate(line):
        if ch == '#':
            walls.add((i, j))
        elif ch == '[':
            # Check if next char is ']'
            if j+1 < scaled_cols and scaled_warehouse[i][j+1] == ']':
                boxes.add((i, j))  # Store boxes by the position of '['
        elif ch == '@':
            robot = (i, j)

def push(box, d):
    """
    Attempt to push the box at position box (which is the '[' of '[]') in direction d.
    If pushing fails, return None. Otherwise, return True.
    """
    assert box in boxes
    nxt = addt(box, d)
    # After pushing:
    # The box currently occupies (box)='[' and (box[0], box[1]+1)=']'
    # After push, it should occupy (nxt)='[' and (nxt[0], nxt[1]+1)=']'
    # Check for walls:
    if nxt in walls or (nxt[0], nxt[1]+1) in walls:
        return None

    # Check if pushing further boxes is needed
    # Vertical push
    if d[0] != 0:
        # Check for boxes in the new positions
        # The pushed box moves to nxt, so check nxt itself:
        if nxt in boxes:
            if push(nxt, d) is None:
                return None
        # Check left and right neighbors if they form boxes
        left_pos = (nxt[0], nxt[1]-1)
        if left_pos in boxes:
            if push(left_pos, d) is None:
                return None
        right_pos = (nxt[0], nxt[1]+1)
        if right_pos in boxes:
            if push(right_pos, d) is None:
                return None

    # Horizontal push
    if d[1] == 1:
        # Pushing right
        if nxt in boxes:
            if push(nxt, d) is None:
                return None

    if d[1] == -1:
        # Pushing left
        if nxt in boxes:
            if push(nxt, d) is None:
                return None

    # Move the box
    boxes.remove(box)
    boxes.add(nxt)
    return True

for move in moves:
    nxt = addt(robot, move)
    if nxt in walls:
        # Can't move robot into walls
        continue

    # If there is a box in nxt or to the left of nxt (for horizontal moves), try pushing
    # Check direct position first
    if nxt in boxes:
        copy_boxes = boxes.copy()
        r = push(nxt, move)
        if r is None:
            boxes = copy_boxes
            continue
    else:
        # Maybe we encountered ']' first if pushing horizontally
        left_nxt = (nxt[0], nxt[1]-1)
        if left_nxt in boxes:
            copy_boxes = boxes.copy()
            r = push(left_nxt, move)
            if r is None:
                boxes = copy_boxes
                continue

    # Move robot
    robot = nxt

# After all moves, compute sum of GPS coordinates
c = 0
for box in boxes:
    # box is at position of '['
    # GPS: 100 * row + col
    c += 100 * box[0] + box[1]

print(c)