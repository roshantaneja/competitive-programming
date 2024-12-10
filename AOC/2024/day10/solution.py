from collections import deque
with open("input.txt") as file:
    lines = file.read().strip().split("\n")

grid = [list(map(int, list(line))) for line in lines]
rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0

directions = [(0,1),(0,-1),(1,0),(-1,0)]

trailheads = []
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 0:
            trailheads.append((r,c))

def reachable_nines_from(r,c):
    queue = deque()
    visited = set()
    if grid[r][c] != 0:
        return set()
    queue.append((r,c,0))
    visited.add((r,c,0))

    found_nines = set()

    while queue:
        x,y,h = queue.popleft()
        if h == 9:
            found_nines.add((x,y))
            continue

        nh = h + 1
        for dx,dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == nh:
                    state = (nx,ny,nh)
                    if state not in visited:
                        visited.add(state)
                        queue.append(state)

    return found_nines

def part1():
    total_score = 0
    for (r,c) in trailheads:
        nines = reachable_nines_from(r,c)
        total_score += len(nines)

    return total_score


print(part1())



def part2():
    ways = {}

    def count_ways(r, c):
        if (r,c) in ways:
            return ways[(r,c)]

        h = grid[r][c]
        if h == 9:
            ways[(r,c)] = 1
            return 1

        total_paths = 0
        nh = h + 1
        for dx,dy in directions:
            nr,nc = r+dx,c+dy
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == nh:
                    total_paths += count_ways(nr, nc)

        ways[(r,c)] = total_paths
        return total_paths

    total_rating = 0
    for r,c in trailheads:
        total_rating += count_ways(r,c)

    return total_rating

print(part2())