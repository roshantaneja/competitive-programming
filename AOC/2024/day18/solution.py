from collections import deque

with open("input.txt") as file:
    lines = file.read().splitlines()

# We need a 71x71 grid (since the problem states 0..70)
SIZE = 71
grid = [[False]*SIZE for _ in range(SIZE)]  # False => safe; True => corrupted

# Parse incoming bytes and mark the first 1024 as corrupted
# Each line is "X,Y"
for i, line in enumerate(lines):
    if i >= 1024:
        break  # Only simulate the first 1024
    x_str, y_str = line.strip().split(',')
    x, y = int(x_str), int(y_str)
    if 0 <= x < SIZE and 0 <= y < SIZE:
        grid[y][x] = True  # Mark corrupted, note y is "row", x is "column"

def bfs_shortest_path(start, end):
    """
    Returns the minimum number of steps from start to end
    using 4-directional moves, or None if no path exists.
    """
    (start_y, start_x) = start
    (end_y, end_x) = end
    
    if grid[start_y][start_x]:
        return None  # can't start if it's corrupted
    if grid[end_y][end_x]:
        return None  # can't end if it's corrupted
    
    visited = [[False]*SIZE for _ in range(SIZE)]
    visited[start_y][start_x] = True
    queue = deque([(start_y, start_x, 0)])  # (row, col, distance)
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == (end_y, end_x):
            return dist
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                if not grid[nr][nc] and not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc, dist + 1))
    
    return None

start_coord = (0, 0)
end_coord = (70, 70)

steps = bfs_shortest_path(start_coord, end_coord)
if steps is None:
    print("No path exists after 1024 bytes have corrupted the memory space.")
else:
    print(f"Minimum number of steps needed: {steps}")






# Part 2
def bfs_shortest_path(start, end):
    """Return True if there's a path, else False."""
    (sy, sx) = start
    (ey, ex) = end
    
    # If start or end is corrupted, no path
    if grid[sy][sx] or grid[ey][ex]:
        return False
    
    visited = [[False]*SIZE for _ in range(SIZE)]
    visited[sy][sx] = True
    
    queue = deque([(sy, sx)])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c = queue.popleft()
        if (r, c) == (ey, ex):
            return True  # Path found
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < SIZE and 0 <= nc < SIZE:
                if not grid[nr][nc] and not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
    
    return False  # No path

start_coord = (0, 0)
end_coord = (70, 70)

# Keep adding bytes one-by-one. After each addition, check if path remains.
for i, line in enumerate(lines):
    x_str, y_str = line.strip().split(',')
    x, y = int(x_str), int(y_str)
    
    # Mark this coordinate as corrupted
    if 0 <= x < SIZE and 0 <= y < SIZE:
        grid[y][x] = True
    
    # Check if path is still possible
    if not bfs_shortest_path(start_coord, end_coord):
        print(f"{x},{y}")
        break
else:
    # If we finish the loop and never break,
    # it means all bytes fell and the path is *still* reachable (unlikely, but possible).
    print("Path remains possible even after all bytes have fallen.")