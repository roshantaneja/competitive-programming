from collections import defaultdict

with open("input.txt") as file:
    lines = file.read().strip().split("\n")

# Parse the input into a grid
grid = [list(line.strip()) for line in lines]
rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0

visited = [[False]*cols for _ in range(rows)]

# Directions for exploring neighbors (up, down, left, right)
directions = [(-1,0), (1,0), (0,-1), (0,1)]

def in_bounds(r, c):
    return 0 <= r < rows and 0 <= c < cols

def part1():
    total_cost = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                stack = [(r,c)]
                visited[r][c] = True

                region_cells = []
                while stack:
                    rr, cc = stack.pop()
                    region_cells.append((rr,cc))
                    for dr, dc in directions:
                        nr, nc = rr+dr, cc+dc
                        if in_bounds(nr, nc) and not visited[nr][nc] and grid[nr][nc] == plant_type:
                            visited[nr][nc] = True
                            stack.append((nr,nc))

                area = len(region_cells)

                perimeter = 0
                for (rr, cc) in region_cells:
                    for dr, dc in directions:
                        nr, nc = rr+dr, cc+dc
                        if not in_bounds(nr, nc) or grid[nr][nc] != plant_type:
                            perimeter += 1

                # Price for this region
                price = area * perimeter
                total_cost += price

    return total_cost

print(part1())

def part2():
    grid = [list(line.strip()) for line in lines]

    regions = []
    for y, row in enumerate(grid):
        for x, plant in enumerate(row):
            if plant != '*':
                regions.append([set(), 0])
                new_plots = {(x, y)}
                vertical_sides = defaultdict(list)
                horizontal_sides = defaultdict(list)

                while new_plots:
                    x1, y1 = new_plots.pop()
                    for x2, y2 in [(x1 + 1, y1), (x1 - 1, y1), (x1, y1 + 1), (x1, y1 - 1)]:
                        out_of_bounds = not (0 <= x2 < len(grid) and 0 <= y2 < len(grid))
                        diff_region = (not out_of_bounds) and (grid[y2][x2] != plant and (grid[y2][x2] != '*' or (x2, y2) not in regions[-1][0]))

                        if out_of_bounds or diff_region:
                            if x2 != x1:
                                vertical_sides[(x1, x2)].append(y1)
                            else:
                                horizontal_sides[(y1, y2)].append(x1)
                        elif not out_of_bounds and grid[y2][x2] == plant and (x2, y2) not in regions[-1][0]:
                            new_plots.add((x2, y2))

                    regions[-1][0].add((x1, y1))
                    grid[y1][x1] = '*'

                for k in list(vertical_sides.values()) + list(horizontal_sides.values()):
                    k.sort()
                    regions[-1][1] += sum(1 for i in range(len(k) - 1) if k[i + 1] - k[i] > 1) + 1

    return sum(len(region[0]) * region[1] for region in regions)

print(part2())