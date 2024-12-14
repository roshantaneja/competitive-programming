with open("input.txt") as file:
    lines = file.read().strip().split("\n")

width = 101
height = 103
time = 100
max_search = 200000

# Parse input data
robots = []
for line in lines:
    pos_part, vel_part = line.split(" v=")
    px, py = map(int, pos_part[2:].split(","))
    vx, vy = map(int, vel_part.split(","))
    robots.append(((px, py), (vx, vy)))


def simulate(robots, time, width, height):
    """
    Simulate robot positions after `time` seconds with wrapping.
    """
    positions = []
    for (px, py), (vx, vy) in robots:
        # Calculate new position after `time` seconds, with wrapping
        new_x = (px + vx * time) % width
        new_y = (py + vy * time) % height
        positions.append((new_x, new_y))
    return positions


def count_quadrants(positions, width, height):
    """
    Count robots in each quadrant.
    """
    mid_x = width // 2
    mid_y = height // 2
    quadrant_counts = [0, 0, 0, 0]  # Top-left, Top-right, Bottom-left, Bottom-right

    for x, y in positions:
        if x == mid_x or y == mid_y:  # Skip robots on the middle lines
            continue
        if x < mid_x and y < mid_y:
            quadrant_counts[0] += 1  # Top-left
        elif x >= mid_x and y < mid_y:
            quadrant_counts[1] += 1  # Top-right
        elif x < mid_x and y >= mid_y:
            quadrant_counts[2] += 1  # Bottom-left
        else:
            quadrant_counts[3] += 1  # Bottom-right

    return quadrant_counts


def part1(robots, time, width, height):
    """
    Simulate robots after 100 seconds and calculate the safety factor.
    """
    positions = simulate(robots, time, width, height)
    quadrant_counts = count_quadrants(positions, width, height)
    safety_factor = 1
    for count in quadrant_counts:
        safety_factor *= count
    return safety_factor


# Run Part 1
safety_factor = part1(robots, time, width, height)
print("Part 1 - Safety Factor:", safety_factor)






with open("input.txt") as file:
    lines = file.read().strip().split("\n")

# Parse input data
robots = []
for line in lines:
    pos_part, vel_part = line.split(" v=")
    px, py = map(int, pos_part[2:].split(","))
    vx, vy = map(int, vel_part.split(","))
    robots.append(((px, py), (vx, vy)))

# Function to get robot positions at a given time
def get_positions_at_time(robots, time, width, height, wrap=True):
    """
    Calculate the positions of robots at a given time.
    If `wrap` is True, positions wrap around the grid.
    """
    positions = []
    for (px, py), (vx, vy) in robots:
        new_x = (px + vx * time) % width if wrap else (px + vx * time)
        new_y = (py + vy * time) % height if wrap else (py + vy * time)
        positions.append((new_x, new_y))
    return positions

# Function to generate the grid visualization
def create_grid(positions, width, height):
    """
    Create a grid representation of robot positions.
    """
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for x, y in positions:
        grid[y % height][x % width] = '#'  # Mark robot position
    return "\n".join("".join(row) for row in grid)

# Write 10,000 steps to a file
output_file = "robot_steps.txt"
width, height = 101, 103  # Dimensions of the space

with open(output_file, "w") as file:
    for step in range(10000):
        file.write(f"STEP {step}\n")
        positions = get_positions_at_time(robots, step, width, height, wrap=False)
        grid = create_grid(positions, width, height)
        file.write(grid + "\n\n")  # Add spacing between steps

print(f"Robot positions for 10,000 steps written to {output_file}.")

