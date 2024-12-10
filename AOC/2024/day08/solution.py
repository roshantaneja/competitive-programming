import re
import math

with open("input.txt") as file:
    lines = [line.rstrip("\n") for line in file]

freq_positions = {}
height = len(lines)
width = len(lines[0]) if height > 0 else 0

# Collect antenna positions by frequency
for r in range(height):
    for c in range(width):
        ch = lines[r][c]
        if ch != '.':
            if ch not in freq_positions:
                freq_positions[ch] = []
            freq_positions[ch].append((r, c))

antinodes = set()
all_antinodes = set()

# For each frequency, consider all pairs of antennas
for freq, positions in freq_positions.items():
    n = len(positions)
    # If only one antenna of this frequency, it contributes no antinodes
    if n == 1:
        continue
    # Every antenna of this frequency is now also an antinode
    for p in positions:
        all_antinodes.add(p)
    processed_lines = set()
    for i in range(n):
        for j in range(i+1, n):
            (r1, c1) = positions[i]
            (r2, c2) = positions[j]
            # Vector from one antenna to the other
            dr = r2 - r1
            dc = c2 - c1
            
            # pt 1
            p1 = (2*r1 - r2, 2*c1 - c2)
            p2 = (2*r2 - r1, 2*c2 - c1)
            
            if 0 <= p1[0] < height and 0 <= p1[1] < width:
                antinodes.add(p1)
            if 0 <= p2[0] < height and 0 <= p2[1] < width:
                antinodes.add(p2)
            

            # pt 2

            g = math.gcd(dr, dc)
            step_r = dr // g
            step_c = dc // g

            rr, cc = r1, c1
            while 0 <= rr - step_r < height and 0 <= cc - step_c < width:
                rr -= step_r
                cc -= step_c
            line_id = (step_r, step_c, rr, cc)
            if line_id in processed_lines:
                continue
            processed_lines.add(line_id)

            # Now generate all points along this line within the grid
            nr, nc = rr, cc
            while 0 <= nr < height and 0 <= nc < width:
                # Any point on this line is an antinode because it's in line with two antennas
                all_antinodes.add((nr, nc))
                nr += step_r
                nc += step_c


print(len(antinodes))
print(len(all_antinodes))