with open("input.txt") as file:
    line = file.read().strip()


def blink(n):
    stones = line.split()
    stones = [int(x) for x in stones]
    memo = {}
    def count_stones_after(stone, steps):
        if steps == 0:
            return 1
        if (stone, steps) in memo:
            return memo[(stone, steps)]

        if stone == 0:
            result = count_stones_after(1, steps - 1)
        else:
            s = str(stone)
            if len(s) % 2 == 0:
                mid = len(s) // 2
                left_part = int(s[:mid])
                right_part = int(s[mid:])
                result = count_stones_after(left_part, steps - 1) + count_stones_after(right_part, steps - 1)
            else:
                new_stone = stone * 2024
                result = count_stones_after(new_stone, steps - 1)

        memo[(stone, steps)] = result
        return result

    total_count = 0
    for st in stones:
        total_count += count_stones_after(st, n)

    return total_count

print(blink(25))
print(blink(75))