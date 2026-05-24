from collections import defaultdict
from pathlib import Path


OPS = (
    lambda r, c: (r, c),
    lambda r, c: (r, -c),
    lambda r, c: (-r, c),
    lambda r, c: (-r, -c),
    lambda r, c: (c, r),
    lambda r, c: (c, -r),
    lambda r, c: (-c, r),
    lambda r, c: (-c, -r),
)

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def parse_grid(path):
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(line.split())
    return rows


def normalize(shape):
    return tuple(sorted(shape))


def build_candidates(grid):
    rows = len(grid)
    cols = len(grid[0])

    clues = defaultdict(set)
    fixed = {}
    n = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "__":
                k = int(grid[r][c])
                clues[k].add((r, c))
                fixed[(r, c)] = k
                if k > n:
                    n = k

    def conflicts_fixed(cell, k):
        fv = fixed.get(cell)
        return fv is not None and fv != k

    def children_of_shape(prev_shape, k):
        prev = list(prev_shape)
        seen = set()
        out = []

        for op in OPS:
            transformed = [op(r, c) for (r, c) in prev]
            min_r = min(r for r, _ in transformed)
            max_r = max(r for r, _ in transformed)
            min_c = min(c for _, c in transformed)
            max_c = max(c for _, c in transformed)

            for dr in range(-min_r, rows - max_r):
                for dc in range(-min_c, cols - max_c):
                    base = set()
                    ok = True
                    for rr, cc in transformed:
                        cell = (rr + dr, cc + dc)
                        if conflicts_fixed(cell, k):
                            ok = False
                            break
                        base.add(cell)
                    if not ok:
                        continue

                    missing = clues[k] - base
                    if len(missing) > 1:
                        continue

                    required_extra = None
                    if missing:
                        required_extra = next(iter(missing))
                        if required_extra in base or conflicts_fixed(required_extra, k):
                            continue

                    frontier = set()
                    for r0, c0 in base:
                        for dr2, dc2 in DIRS:
                            nr, nc = r0 + dr2, c0 + dc2
                            cell = (nr, nc)
                            if (
                                0 <= nr < rows
                                and 0 <= nc < cols
                                and cell not in base
                                and not conflicts_fixed(cell, k)
                            ):
                                frontier.add(cell)

                    if required_extra is not None:
                        if required_extra not in frontier:
                            continue
                        shape = normalize(base | {required_extra})
                        if shape not in seen:
                            seen.add(shape)
                            out.append(shape)
                    else:
                        for extra in frontier:
                            shape = normalize(base | {extra})
                            if clues[k].issubset(shape) and shape not in seen:
                                seen.add(shape)
                                out.append(shape)

        return out

    shapes = {}
    shapes[1] = [normalize({next(iter(clues[1]))})]

    fwd = {}
    rev = {}
    for k in range(2, n + 1):
        next_shapes = []
        shape_to_id = {}
        fwd[k - 1] = defaultdict(list)
        rev[k] = defaultdict(list)

        for parent_id, parent_shape in enumerate(shapes[k - 1]):
            for child_shape in children_of_shape(parent_shape, k):
                child_id = shape_to_id.get(child_shape)
                if child_id is None:
                    child_id = len(next_shapes)
                    shape_to_id[child_shape] = child_id
                    next_shapes.append(child_shape)
                fwd[k - 1][parent_id].append(child_id)
                rev[k][child_id].append(parent_id)

        shapes[k] = next_shapes

    return n, shapes, fwd, rev


def arc_consistency(domains, n, fwd, rev):
    changed = True
    while changed:
        changed = False
        for k in range(2, n + 1):
            allowed_k = set()
            for parent_id in domains[k - 1]:
                for child_id in fwd[k - 1].get(parent_id, ()):
                    allowed_k.add(child_id)

            new_dom_k = domains[k] & allowed_k
            if new_dom_k != domains[k]:
                domains[k] = new_dom_k
                changed = True
            if not domains[k]:
                return False

            allowed_prev = set()
            for child_id in domains[k]:
                for parent_id in rev[k].get(child_id, ()):
                    allowed_prev.add(parent_id)

            new_dom_prev = domains[k - 1] & allowed_prev
            if new_dom_prev != domains[k - 1]:
                domains[k - 1] = new_dom_prev
                changed = True
            if not domains[k - 1]:
                return False

    return True


def solve(grid):
    n, shapes, fwd, rev = build_candidates(grid)

    domains = {}
    for k in range(1, n + 1):
        domains[k] = set(range(len(shapes[k])))
    if not arc_consistency(domains, n, fwd, rev):
        return None, None

    assigned = {}
    occupied = set()

    def adjacent_ok(k, shape_id):
        if k > 1 and (k - 1) in assigned:
            if shape_id not in fwd[k - 1].get(assigned[k - 1], ()):
                return False
        if k < n and (k + 1) in assigned:
            if assigned[k + 1] not in fwd[k].get(shape_id, ()):
                return False
        return True

    def backtrack(curr_domains):
        if len(assigned) == n:
            return True

        k = min(
            (kk for kk in range(1, n + 1) if kk not in assigned),
            key=lambda kk: len(curr_domains[kk]),
        )

        for shape_id in list(curr_domains[k]):
            shape = shapes[k][shape_id]

            conflict = False
            for cell in shape:
                if cell in occupied:
                    conflict = True
                    break
            if conflict:
                continue

            if not adjacent_ok(k, shape_id):
                continue

            assigned[k] = shape_id
            for cell in shape:
                occupied.add(cell)

            next_domains = {}
            for kk in range(1, n + 1):
                next_domains[kk] = set(curr_domains[kk])
            next_domains[k] = {shape_id}

            consistent = True
            for kk in range(1, n + 1):
                if kk in assigned:
                    continue
                filtered = set()
                for sid in next_domains[kk]:
                    sh = shapes[kk][sid]
                    bad = False
                    for cell in sh:
                        if cell in occupied:
                            bad = True
                            break
                    if not bad:
                        filtered.add(sid)
                next_domains[kk] = filtered
                if not filtered:
                    consistent = False
                    break

            if consistent and arc_consistency(next_domains, n, fwd, rev):
                if backtrack(next_domains):
                    return True

            del assigned[k]
            for cell in shape:
                occupied.remove(cell)

        return False

    if not backtrack(domains):
        return None, None

    solution_shapes = {}
    for k in range(1, n + 1):
        solution_shapes[k] = shapes[k][assigned[k]]
    return n, solution_shapes


def main():
    grid = parse_grid(Path(__file__).with_name("input.txt"))
    n, solution_shapes = solve(grid)
    if n is None:
        print("No solution found.")
        return

    rows = len(grid)
    cols = len(grid[0])
    out = [["__"] * cols for _ in range(rows)]

    for k in range(1, n + 1):
        for r, c in solution_shapes[k]:
            out[r][c] = f"{k:02d}"

    row_sums = []
    for r in range(rows):
        s = 0
        for c in range(cols):
            if out[r][c] != "__":
                s += int(out[r][c])
        row_sums.append(s)
        print(" ".join(out[r]), "|", s)

    low = min(row_sums)
    high = max(row_sums)
    print()
    print("N:", n)
    print("min row sum:", low)
    print("max row sum:", high)
    print("answer:", low * high)


if __name__ == "__main__":
    main()
