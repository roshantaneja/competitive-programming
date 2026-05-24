"""
Animated visualizer for the vanilla backtracking solver.
Shows the search in real-time: each placement and backtrack as the solver explores.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from solver_vanilla import parse_grid, build_candidates, arc_consistency


def get_color_for_k(k: int, n: int) -> tuple[float, float, float, float]:
    """Return RGBA for k-omino."""
    cmap = plt.colormaps["nipy_spectral"]
    t = (k - 1) / max(n, 1) if n > 0 else 0
    return cmap(t)


def solve_with_animation(grid):
    """
    Same logic as solver_vanilla.solve, but yields (grid_state, event) at each step.
    grid_state: rows x cols, value k or 0 for empty
    event: "try" | "place" | "backtrack" | "solution"
    """
    n, shapes, fwd, rev = build_candidates(grid)
    rows = len(grid)
    cols = len(grid[0])

    domains = {}
    for k in range(1, n + 1):
        domains[k] = set(range(len(shapes[k])))
    if not arc_consistency(domains, n, fwd, rev):
        yield None, "fail"
        return

    assigned = {}
    occupied = set()

    def assigned_to_grid():
        g = [[0] * cols for _ in range(rows)]
        for k, shape_id in assigned.items():
            for r, c in shapes[k][shape_id]:
                g[r][c] = k
        return g

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
            yield assigned_to_grid(), "solution"
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

            # Try placing - yield "try" then "place"
            yield assigned_to_grid(), "try"
            assigned[k] = shape_id
            for cell in shape:
                occupied.add(cell)
            yield assigned_to_grid(), "place"

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
                for state, evt in backtrack(next_domains):
                    yield state, evt
                    if evt == "solution":
                        return True

            # Backtrack
            del assigned[k]
            for cell in shape:
                occupied.remove(cell)
            yield assigned_to_grid(), "backtrack"

        return False

    # Initial state
    yield assigned_to_grid(), "start"

    gen = backtrack(domains)
    for state, evt in gen:
        yield state, evt
        if evt == "solution":
            return

    yield assigned_to_grid(), "fail"


def main():
    input_path = Path(__file__).with_name("input.txt")
    grid_str = parse_grid(input_path)
    rows = len(grid_str)
    cols = len(grid_str[0])

    # Collect all frames
    print("Running backtracking solver (collecting animation frames)...")
    frames = []
    n = None
    for state, event in solve_with_animation(grid_str):
        if state is None:
            break
        # Infer n from the first non-empty state
        if n is None and state:
            n = max(max(row) for row in state) if any(any(row) for row in state) else 16
        if n is None:
            n = 16
        frames.append((state, event))
        if event == "solution":
            break
        if event == "fail":
            print("No solution found.")
            return

    if not frames:
        print("No solution found.")
        return

    n = max(n, max(max(row) for row in frames[-1][0]))
    print(f"Collected {len(frames)} frames. Building animation...")

    # Setup figure
    fig, ax = plt.subplots(1, 1, figsize=(max(8, cols * 0.6), max(6, rows * 0.5)))
    cmap = plt.colormaps["nipy_spectral"]

    def build_image(state):
        color_grid = np.zeros((rows, cols, 4))
        for r in range(rows):
            for c in range(cols):
                k = state[r][c]
                if k > 0:
                    color_grid[r, c] = get_color_for_k(k, n)
                else:
                    color_grid[r, c] = (0.95, 0.95, 0.95, 1)
        return color_grid

    im = ax.imshow(build_image(frames[0][0]), aspect="equal")
    ax.set_xticks(np.arange(cols))
    ax.set_yticks(np.arange(rows))
    ax.set_xticklabels(np.arange(cols))
    ax.set_yticklabels(np.arange(rows))
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    for x in range(cols + 1):
        ax.axvline(x - 0.5, color="gray", linewidth=0.5)
    for y in range(rows + 1):
        ax.axhline(y - 0.5, color="gray", linewidth=0.5)

    title = ax.set_title("")

    # Text labels for cells (updated each frame)
    texts = [[ax.text(c, r, "", ha="center", va="center", fontsize=7) for c in range(cols)] for r in range(rows)]

    def update(frame_idx):
        state, event = frames[frame_idx]
        im.set_array(build_image(state))
        event_labels = {"start": "Starting...", "try": "Trying placement", "place": "Placed", "backtrack": "Backtracking", "solution": "Solution found!"}
        title.set_text(f"Frame {frame_idx + 1}/{len(frames)} — {event_labels.get(event, event)}")
        for r in range(rows):
            for c in range(cols):
                k = state[r][c]
                texts[r][c].set_text(str(k) if k > 0 else "")
                texts[r][c].set_color("white" if k > 0 and np.mean(get_color_for_k(k, n)[:3]) < 0.5 else "black")
        return [im, title] + [t for row in texts for t in row]

    # Throttle: for large animations, don't show every frame
    step = max(1, len(frames) // 300)  # aim for ~300 frames max
    indices = list(range(0, len(frames), step))
    if indices[-1] != len(frames) - 1:
        indices.append(len(frames) - 1)  # always include last frame

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=indices,
        interval=30,
        blit=False,
        repeat=False,
    )

    plt.tight_layout()
    output_path = Path(__file__).with_name("subtiles_animation.gif")
    print(f"Saving animation to {output_path.name} (this may take a moment)...")
    ani.save(output_path, writer="pillow", fps=30, dpi=80)
    print("Done!")
    plt.show()


if __name__ == "__main__":
    main()
