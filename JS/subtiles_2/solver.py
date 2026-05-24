from collections import defaultdict
from pathlib import Path

from ortools.sat.python import cp_model


def parse_grid(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(line.split())
    return rows


def get_symmetry_ops():
    return [
        lambda r, c: (r, c),
        lambda r, c: (r, -c),
        lambda r, c: (-r, c),
        lambda r, c: (-r, -c),
        lambda r, c: (c, r),
        lambda r, c: (c, -r),
        lambda r, c: (-c, r),
        lambda r, c: (-c, -r),
    ]


def build_model(grid: list[list[str]], n: int = 16):
    r_count = len(grid)
    c_count = len(grid[0])

    model = cp_model.CpModel()
    x = {}
    for r in range(r_count):
        for c in range(c_count):
            for k in range(1, n + 1):
                x[r, c, k] = model.NewBoolVar(f"x_{r}_{c}_{k}")

    fixed_by_pos: dict[tuple[int, int], int] = {}
    clues_by_value: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for r in range(r_count):
        for c in range(c_count):
            if grid[r][c] != "__":
                k = int(grid[r][c])
                fixed_by_pos[r, c] = k
                clues_by_value[k].append((r, c))

    # Each cell has at most one label.
    for r in range(r_count):
        for c in range(c_count):
            model.Add(sum(x[r, c, k] for k in range(1, n + 1)) <= 1)
            if (r, c) in fixed_by_pos:
                model.Add(x[r, c, fixed_by_pos[r, c]] == 1)

    # Exactly k cells labeled k.
    for k in range(1, n + 1):
        model.Add(sum(x[r, c, k] for r in range(r_count) for c in range(c_count)) == k)

    # Connectivity via single-commodity flow for every k.
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for k in range(1, n + 1):
        has_clue = len(clues_by_value[k]) > 0
        root = {}
        if has_clue:
            rr, cc = clues_by_value[k][0]
            model.Add(x[rr, cc, k] == 1)
            for r in range(r_count):
                for c in range(c_count):
                    root[r, c] = model.NewBoolVar(f"root_{k}_{r}_{c}")
                    if (r, c) == (rr, cc):
                        model.Add(root[r, c] == 1)
                    else:
                        model.Add(root[r, c] == 0)
        else:
            for r in range(r_count):
                for c in range(c_count):
                    root[r, c] = model.NewBoolVar(f"root_{k}_{r}_{c}")
                    model.Add(root[r, c] <= x[r, c, k])
            model.Add(sum(root[r, c] for r in range(r_count) for c in range(c_count)) == 1)

        f = {}
        for r in range(r_count):
            for c in range(c_count):
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < r_count and 0 <= nc < c_count:
                        edge = (r, c, nr, nc)
                        f[edge] = model.NewIntVar(0, k - 1, f"f_{k}_{r}_{c}_{nr}_{nc}")
                        model.Add(f[edge] <= (k - 1) * x[r, c, k])
                        model.Add(f[edge] <= (k - 1) * x[nr, nc, k])

        for r in range(r_count):
            for c in range(c_count):
                inflow = []
                outflow = []
                for dr, dc in dirs:
                    pr, pc = r + dr, c + dc
                    if 0 <= pr < r_count and 0 <= pc < c_count:
                        inflow.append(f[pr, pc, r, c])
                        outflow.append(f[r, c, pr, pc])

                # For selected non-root cells, demand is 1.
                # The root supplies (k-1) units.
                model.Add(sum(inflow) - sum(outflow) == x[r, c, k] - k * root[r, c])

    # Containment: for each k>1, K contains a transformed copy of (K-1).
    # We pre-prune transform+translation candidates using fixed clues.
    symmetry_ops = get_symmetry_ops()
    for k in range(2, n + 1):
        candidates = []
        max_shift_r = 2 * (r_count - 1)
        max_shift_c = 2 * (c_count - 1)
        for op_idx, op in enumerate(symmetry_ops):
            for dr in range(-max_shift_r, max_shift_r + 1):
                for dc in range(-max_shift_c, max_shift_c + 1):
                    valid = True
                    for rr, cc in clues_by_value[k - 1]:
                        tr, tc = op(rr, cc)
                        tr += dr
                        tc += dc
                        if not (0 <= tr < r_count and 0 <= tc < c_count):
                            valid = False
                            break
                        fixed = fixed_by_pos.get((tr, tc))
                        if fixed is not None and fixed != k:
                            valid = False
                            break
                    if valid:
                        candidates.append((op_idx, dr, dc))

        y = []
        for idx, (op_idx, dr, dc) in enumerate(candidates):
            choose = model.NewBoolVar(f"contain_{k}_{idx}")
            y.append(choose)
            op = symmetry_ops[op_idx]

            for r in range(r_count):
                for c in range(c_count):
                    tr, tc = op(r, c)
                    tr += dr
                    tc += dc
                    if 0 <= tr < r_count and 0 <= tc < c_count:
                        model.Add(x[r, c, k - 1] <= x[tr, tc, k]).OnlyEnforceIf(choose)
                    else:
                        model.Add(x[r, c, k - 1] == 0).OnlyEnforceIf(choose)

        model.Add(sum(y) == 1)

    return model, x


def solve(grid: list[list[str]], n: int):
    model, x = build_model(grid, n)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 180
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    return status, solver, x


def main():
    input_path = Path(__file__).with_name("input.txt")
    grid = parse_grid(input_path)

    solved_n = None
    status = cp_model.UNKNOWN
    solver = None
    x = None
    for candidate_n in (17, 16):
        status, solver, x = solve(grid, n=candidate_n)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            solved_n = candidate_n
            break

    if solved_n is None:
        print("No solution found for N=16 or N=17.")
        return

    r_count = len(grid)
    c_count = len(grid[0])
    row_sums = []
    solved_rows = []
    for r in range(r_count):
        row = []
        s = 0
        for c in range(c_count):
            val = "__"
            for k in range(1, solved_n + 1):
                if solver.Value(x[r, c, k]):
                    val = f"{k:02d}"
                    s += k
                    break
            row.append(val)
        solved_rows.append(row)
        row_sums.append(s)

    for row, s in zip(solved_rows, row_sums):
        print(" ".join(row), "|", s)

    answer = min(row_sums) * max(row_sums)
    print()
    print("N:", solved_n)
    print("min row sum:", min(row_sums))
    print("max row sum:", max(row_sums))
    print("answer:", answer)


if __name__ == "__main__":
    main()

