import pathlib

directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

# grid = []
# for i in range(len(content)):
#     content[i] = content[i][:-1]
#     grid.append([])
#     for j in range(len(content[i])):
#         grid[i].append(int(content[i][j]))

grid = []
with open('input.txt') as f:
    for line in f.readlines():
        grid.append(list(map(int, line.strip())))

#literally refused to read the last number so now i have to manually add it
#grid[98].append(1)
#grid[4].append(0)


def isVisible(i, j):
    m = len(grid)
    n = len(grid[0])
    for di, dj in directions:
        ni, nj = i + di, j + dj

        while 0 <= ni < m and 0 <= nj < n and grid[ni][nj] < grid[i][j]:
            ni += di
            nj += dj

        if not(0 <= ni < m and 0 <= nj < n):
            return True
    return False

# part 1
total = 0
for i in range(len(grid)):
    for j in range (len(grid[i])):
        if isVisible(i, j):
            total += 1
print (total)

total2 = 0
m = len(grid)
n = len(grid[0])


def score(i, j):
    s = 1
    for di, dj in directions:
        curr = 0
        ni, nj = i + di, j + dj

        while 0 <= ni < m and 0 <= nj < n:
            curr += 1
            if grid[ni][nj] >= grid[i][j]:
                break

            ni += di
            nj += dj

        s *= curr

    return s

# part 2
for i in range(m):
    for j in range(n):
        print(score(i, j))
        total2 = max(total2, score(i, j))
print (total2)
print ("hello")