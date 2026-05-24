"""
Place a digit in each of the 25 spots in the below 5×5 grid, so that each 5-digit number (leading zeroes are ok) reading across and reading down is divisible by the number outside the grid, trying to maximize the sum of the 25 numbers you enter.

Constraints (divisibility rules used):
- Row 1 div 1: any
- Row 2 div 2: last digit even
- Row 3 div 3: digit sum div by 3
- Row 4 div 4: last 2 digits form number div by 4
- Row 5 div 5: last digit 0 or 5; Col 5 div 10 => grid[4][4]=0 (intersection)
- Col 1 div 6: div by 2 and 3
- Col 2 div 7: no simple rule
- Col 3 div 8: last 3 digits div by 8
- Col 4 div 9: digit sum div by 9
- Col 5 div 10: last digit 0

Optimizations:
1. Row 5 uniquely determined by rows 0-3 (each col's 5th digit forced by divisibility)
2. Precompute valid row numbers, filter row 5 to last digit 0 (row∩col intersection)
3. Modular prefix extendability: (-(P*10+d)*10^(4-L))%div < 10^(4-L) for valid next digit d
4. Try high digit-sum rows first for early pruning
5. Before placing row, filter to digits that keep each column's prefix extendable
"""

import sys
import time

ROW_DIVISORS = [1, 2, 3, 4, 5]
COL_DIVISORS = [6, 7, 8, 9, 10]

DEBUG = "--debug" in sys.argv or "-d" in sys.argv
LIVE_VIEW = "--live" in sys.argv or "-l" in sys.argv  # Show current grid state periodically

if "--help" in sys.argv or "-h" in sys.argv:
    print("Usage: python solver.py [options]")
    print("  -d, --debug   Show progress (nodes, best sum, solutions found)")
    print("  -l, --live    Show current grid state every 2 seconds")
    print("  -h, --help    Show this help")
    sys.exit(0)

RULES = [
    (1, lambda dg: True),
    (2, lambda dg: dg[4] % 2 == 0),
    (3, lambda dg: sum(dg) % 3 == 0),
    (4, lambda dg: dg[-2:] % 4 == 0),
    (5, lambda dg: dg[4] == 0 or dg[4] == 5),
    (6, lambda dg: dg[4] % 2 == 0 and dg[4] % 3 == 0),
    (7, lambda dg: True),
    (8, lambda dg: dg[-3:] % 8 == 0),
    (9, lambda dg: sum(dg) % 9 == 0),
    (10, lambda dg: dg[4] == 0),
]


def digits_of(n):
    return tuple((n // (10 ** (4 - i))) % 10 for i in range(5))


def print_grid(grid, title="", clear=False, filled_rows=5):
    """Print grid state; use _ for unfilled cells. filled_rows=number of rows with real data."""
    if clear:
        print("\033[F" * 12, end="")  # Move cursor up 12 lines
    if title:
        print(title)
    for r in range(5):
        row = []
        for c in range(5):
            if r >= filled_rows:
                row.append("_")
            else:
                v = grid[r][c] if r < len(grid) and c < len(grid[r]) else -1
                row.append(str(v) if v >= 0 else "_")
        print(" ".join(row) + f" |{ROW_DIVISORS[r]:02d}")
    print("-" * 16)
    print(" ".join(f"{COL_DIVISORS[c]:02d}" for c in range(5)))


def precompute_valid_rows():
    result = {d: [] for d in ROW_DIVISORS}
    for num in range(100000):
        dg = digits_of(num)
        for d in ROW_DIVISORS:
            if num % d == 0:
                result[d].append((dg, sum(dg)))
    # Row 5 ∩ Col 5: grid[4][4]=0 (div 5 and div 10)
    result[5] = [(dg, s) for dg, s in result[5] if dg[4] == 0]
    for d in result:
        result[d].sort(key=lambda x: -x[1])
    return result


def solve(debug=False, live_view=False):
    valid_rows = precompute_valid_rows()
    best_sum = -1
    best_grid = None
    grid = [[0] * 5 for _ in range(5)]

    # Debug stats
    nodes_explored = [0]
    solutions_found = [0]
    last_print = [time.perf_counter()]
    last_grid_print = [time.perf_counter()]

    def compute_row4():
        """Row 4 uniquely determined: each col needs (prefix*10+d)%div==0 => d=(-prefix*10)%div."""
        row4 = [0] * 5
        for c in range(5):
            p = sum(grid[r][c] * (10 ** (3 - r)) for r in range(4))
            d = (-p * 10) % COL_DIVISORS[c]
            if d >= 10:
                return None
            row4[c] = d
        return row4

    def valid_next_digits(c, row_count):
        """Digits d that keep column c's prefix extendable."""
        p = sum(grid[r][c] * (10 ** (row_count - 1 - r)) for r in range(row_count))
        return {d for d in range(10) if ((-(p * 10 + d) * pow(10, 4 - row_count, COL_DIVISORS[c])) % COL_DIVISORS[c]) < 10 ** (4 - row_count)}

    def backtrack(row_idx, current_sum):
        nonlocal best_sum, best_grid
        nodes_explored[0] += 1

        if debug or live_view:
            now = time.perf_counter()
            if debug and now - last_print[0] >= 0.5:
                last_print[0] = now
                best_str = str(best_sum) if best_sum >= 0 else "--"
                print(f"\r  Row {row_idx} | nodes: {nodes_explored[0]:,} | best: {best_str} | solutions: {solutions_found[0]}", end="", flush=True)
            if live_view and now - last_grid_print[0] >= 2.0:
                last_grid_print[0] = now
                print()
                best_str = str(best_sum) if best_sum >= 0 else "--"
                print_grid(grid, title=f"Exploring row {row_idx} | nodes: {nodes_explored[0]:,} | best: {best_str}", filled_rows=row_idx)
                print()

        if row_idx == 4:
            row4 = compute_row4()
            if row4 is None or row4[4] != 0 or sum(row4[i] * (10 ** (4 - i)) for i in range(5)) % 5 != 0:
                return
            grid[4] = row4
            s = current_sum + sum(row4)
            solutions_found[0] += 1
            if s > best_sum:
                best_sum = s
                best_grid = [r[:] for r in grid]
                if debug:
                    print()
                    print_grid(grid, title=f"New best! Sum = {s}")
                    print()
            return

        if current_sum + (4 - row_idx) * 45 + 45 <= best_sum:
            return

        div = ROW_DIVISORS[row_idx]
        valid_sets = [valid_next_digits(c, row_idx) for c in range(5)]

        for digits, digit_sum in valid_rows[div]:
            if all(digits[c] in valid_sets[c] for c in range(5)):
                grid[row_idx] = list(digits)
                backtrack(row_idx + 1, current_sum + digit_sum)
        grid[row_idx] = [0] * 5

    if debug or live_view:
        print("Starting search...")
        if debug:
            print("(Progress updates every 0.5s; grid shown when new best found)")
        if live_view:
            print("(Live grid view every 2s)")
        print()
    start = time.perf_counter()
    backtrack(0, 0)
    if debug:
        print()
        print(f"Done in {time.perf_counter() - start:.1f}s | {nodes_explored[0]:,} nodes | {solutions_found[0]} solutions")
    return best_sum, best_grid


def main():
    best_sum, best_grid = solve(debug=DEBUG, live_view=LIVE_VIEW)
    digits = "".join(str(best_grid[r][c]) for r in range(5) for c in range(5))
    print(f"Answer: ({best_sum}, {digits})")
    print("\nGrid:")
    for r in range(5):
        print(" ".join(str(best_grid[r][c]) for c in range(5)) + f" |{ROW_DIVISORS[r]:02d}")
    print("-" * 16)
    print(" ".join(f"{COL_DIVISORS[c]:02d}" for c in range(5)))


if __name__ == "__main__":
    main()
