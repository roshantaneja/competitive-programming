import re

def count_occurrences(grid, word):
    word_len = len(word)
    count = 0
    rows = len(grid)
    cols = len(grid[0])

    def check_word(r, c, dr, dc):
        for i in range(word_len):
            nr, nc = r + i * dr, c + i * dc
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nc] != word[i]:
                return False
        return True

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == word[0]:
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
                for dr, dc in directions:
                    if check_word(r, c, dr, dc):
                        count += 1
    return count

with open('input.txt', 'r') as file:
    lines = file.readlines()

grid = [line.strip() for line in lines]

word = "XMAS"
result = count_occurrences(grid, word)

print(result)


def count_xmas_patterns(grid):
    count = 0
    rows = len(grid)
    cols = len(grid[0])

    def is_xmas(r, c):
        if grid[r][c] != 'A':
            return False
        diag1 = grid[r - 1][c - 1] + grid[r][c] + grid[r + 1][c + 1]
        if diag1 not in {"MAS", "SAM"}:
            return False
        
        diag2 = grid[r - 1][c + 1] + grid[r][c] + grid[r + 1][c - 1]
        if diag2 not in {"MAS", "SAM"}:
            return False
        
        return True

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if is_xmas(r, c):
                count += 1

    return count

with open('input.txt', 'r') as file:
    lines = file.readlines()

grid = [line.strip() for line in lines]

result = count_xmas_patterns(grid)

print(result)