with open("input.txt") as file:
    lines = file.read().splitlines()

# Parse the input maze
maze = lines
rows = len(maze)
cols = len(maze[0])

# Find start (S) and end (E) positions
start = None
end = None
for r in range(rows):
    for c in range(cols):
        if maze[r][c] == 'S':
            start = (r, c)
        elif maze[r][c] == 'E':
            end = (r, c)

# Directions: 0 = North, 1 = East, 2 = South, 3 = West
# Start facing East (1)
start_dir = 1

# Movement deltas for moving forward based on direction
deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

import heapq

def part1():
    # We'll use Dijkstra's algorithm, as we have differing costs
    # State: (cost, row, col, dir)
    # cost: integer
    # We'll keep track of visited states: dist[row][col][dir]
    
    dist = [[[float('inf')] * 4 for _ in range(cols)] for __ in range(rows)]
    dist[start[0]][start[1]][start_dir] = 0

    pq = []
    heapq.heappush(pq, (0, start[0], start[1], start_dir))

    while pq:
        cost, r, c, d = heapq.heappop(pq)
        if cost > dist[r][c][d]:
            continue
        if (r, c) == end:
            return cost

        # Try moving forward
        dr, dc = deltas[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
            # Move forward cost = 1
            ncost = cost + 1
            if ncost < dist[nr][nc][d]:
                dist[nr][nc][d] = ncost
                heapq.heappush(pq, (ncost, nr, nc, d))

        # Turn left (cost 1000)
        nd_left = (d - 1) % 4
        left_cost = cost + 1000
        if left_cost < dist[r][c][nd_left]:
            dist[r][c][nd_left] = left_cost
            heapq.heappush(pq, (left_cost, r, c, nd_left))

        # Turn right (cost 1000)
        nd_right = (d + 1) % 4
        right_cost = cost + 1000
        if right_cost < dist[r][c][nd_right]:
            dist[r][c][nd_right] = right_cost
            heapq.heappush(pq, (right_cost, r, c, nd_right))

print(part1())


import heapq

with open("input.txt") as file:
    lines = file.read().splitlines()

maze = lines
rows = len(maze)
cols = len(maze[0])

# Find S and E positions
start = None
end = None
for r in range(rows):
    for c in range(cols):
        if maze[r][c] == 'S':
            start = (r, c)
        elif maze[r][c] == 'E':
            end = (r, c)

# Directions: 0 = North, 1 = East, 2 = South, 3 = West
# Start facing East
start_dir = 1

# Movement deltas for moving forward
deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def in_bounds(r, c):
    return 0 <= r < rows and 0 <= c < cols

def neighbors_forward(r, c, d):
    """
    Given (r, c, d), yield possible next states (nr, nc, nd, cost).
    Forward movement = cost 1
    Turn left or right = cost 1000
    """
    # Move forward
    dr, dc = deltas[d]
    nr, nc = r + dr, c + dc
    if in_bounds(nr, nc) and maze[nr][nc] != '#':
        yield (nr, nc, d, 1)

    # Turn left
    yield (r, c, (d - 1) % 4, 1000)
    # Turn right
    yield (r, c, (d + 1) % 4, 1000)

def neighbors_reverse(r, c, d):
    """
    Reversed transitions: given (r, c, d), yield the states
    that could move *forward* in the normal sense to (r, c, d).
    
    In forward mode:
      - (r, c, d) -> (r+dr, c+dc, d) cost=1
      - (r, c, d) -> (r, c, d+/-1) cost=1000
      
    So here, if (X, Y, d) -> (r, c, d) by forward movement, 
    then (r, c, d) -> (X, Y, d) in reverse with the same cost.
    """
    # Reverse of forward movement: 
    # If in forward direction we do (r0, c0, d) -> (r0 + dr, c0 + dc, d) with cost=1,
    # then in reverse we do (r, c, d) -> (r - dr, c - dc, d) with cost=1.
    dr, dc = deltas[d]
    rr, cc = r - dr, c - dc
    if in_bounds(rr, cc) and maze[rr][cc] != '#':
        yield (rr, cc, d, 1)
    
    # Reverse of turning left or right (cost 1000):
    # If forward is: (r, c, old_d) -> (r, c, d) with cost=1000 for old_d != d,
    # we just need old_d = (d +/- 1) mod 4.
    # So from (r, c, d), we can go to (r, c, d +/- 1) with cost=1000.
    left_d = (d + 1) % 4   # reversing a left turn
    right_d = (d - 1) % 4  # reversing a right turn
    yield (r, c, left_d, 1000)
    yield (r, c, right_d, 1000)

def dijkstra(starts, get_neighbors):
    """
    Generic Dijkstra to compute minimal cost from 'starts' (a list of (r, c, d, cost=0))
    using the provided 'get_neighbors' function to generate transitions.
    Returns dist[r][c][d] = minimal cost to reach (r, c, d).
    """
    dist = [[[float('inf')] * 4 for _ in range(cols)] for __ in range(rows)]
    pq = []

    # Initialize the queue with the starting states
    for (r, c, d) in starts:
        dist[r][c][d] = 0
        heapq.heappush(pq, (0, r, c, d))

    while pq:
        cur_cost, r, c, d = heapq.heappop(pq)
        if cur_cost > dist[r][c][d]:
            continue

        for (nr, nc, nd, step_cost) in get_neighbors(r, c, d):
            new_cost = cur_cost + step_cost
            if new_cost < dist[nr][nc][nd]:
                dist[nr][nc][nd] = new_cost
                heapq.heappush(pq, (new_cost, nr, nc, nd))

    return dist

def part1():
    # 1) Dijkstra from S in the forward direction (start_dir only)
    # Only one starting direction: facing East at (start[0], start[1], start_dir)
    distS = dijkstra([(start[0], start[1], start_dir)], neighbors_forward)
    # minimal cost is min(distS[end_row][end_col][d] for d in [0..3])
    return min(distS[end[0]][end[1]][d] for d in range(4))

def part2():
    # 1) Forward pass: distS
    distS = dijkstra([(start[0], start[1], start_dir)], neighbors_forward)
    # 2) Reverse pass: distE 
    #    We'll start from E in all 4 directions with cost 0
    #    because we don't care what direction we end up in at E.
    distE = dijkstra([(end[0], end[1], d) for d in range(4)], neighbors_reverse)
    
    # overall minimal cost from S to E
    best_cost = min(distS[end[0]][end[1]][d] for d in range(4))
    
    # Now figure out which tiles (r, c) are on *at least one* of the best paths.
    count = 0
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == '#' or not in_bounds(r, c):
                continue
            # If there exists a direction d for which distS[r][c][d] + distE[r][c][d] == best_cost,
            # then (r,c) is on at least one best path.
            for d in range(4):
                if distS[r][c][d] + distE[r][c][d] == best_cost:
                    count += 1
                    break  # no need to check other directions
    return count

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())

