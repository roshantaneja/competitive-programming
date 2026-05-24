"""
Visualizer for the CP-SAT subtiles solver.
Color-codes each k-omino with a distinct color and displays solutions as they are found.

Note: CP-SAT does not expose partial assignments during search, so we can only visualize
complete solutions. For an animated view of the search (placements and backtracks),
use visualizer_vanilla.py with the backtracking solver.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from ortools.sat.python import cp_model

from solver import parse_grid, build_model


# Distinct color palette for k-ominos (1..N). Using tab20 + Set3 for many distinct colors.
def get_color_for_k(k: int, n: int) -> tuple[float, float, float, float]:
    """Return RGBA for k-omino. Uses a consistent colormap across solutions."""
    cmap = plt.colormaps["nipy_spectral"]
    # Normalize k to [0, 1] avoiding the extremes for better visibility
    t = (k - 1) / max(n, 1) if n > 0 else 0
    return cmap(t)


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    """Collects each solution found during search for visualization."""

    def __init__(self, x: dict, r_count: int, c_count: int, n: int):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._x = x
        self._r_count = r_count
        self._c_count = c_count
        self._n = n
        self.solutions: list[list[list[int]]] = []

    def on_solution_callback(self) -> None:
        """Extract grid assignment for current solution."""
        grid = [[0] * self._c_count for _ in range(self._r_count)]
        for r in range(self._r_count):
            for c in range(self._c_count):
                for k in range(1, self._n + 1):
                    if self.BooleanValue(self._x[r, c, k]):
                        grid[r][c] = k
                        break
        self.solutions.append(grid)


def visualize_solution(
    grid: list[list[int]],
    n: int,
    title: str = "Subtiles solution",
    ax=None,
) -> None:
    """Draw the grid with color-coded k-ominos."""
    r_count = len(grid)
    c_count = len(grid[0])

    # Build color matrix (RGBA for each cell)
    color_grid = np.zeros((r_count, c_count, 4))
    for r in range(r_count):
        for c in range(c_count):
            k = grid[r][c]
            if k > 0:
                color_grid[r, c] = get_color_for_k(k, n)
            else:
                color_grid[r, c] = (1, 1, 1, 1)  # white for empty

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(max(6, c_count * 0.6), max(5, r_count * 0.5)))

    ax.imshow(color_grid, aspect="equal")
    ax.set_xticks(np.arange(c_count))
    ax.set_yticks(np.arange(r_count))
    ax.set_xticklabels(np.arange(c_count))
    ax.set_yticklabels(np.arange(r_count))
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    for edge in ["top", "bottom", "left", "right"]:
        ax.spines[edge].set_visible(True)

    # Draw grid lines
    for x in range(c_count + 1):
        ax.axvline(x - 0.5, color="gray", linewidth=0.5)
    for y in range(r_count + 1):
        ax.axhline(y - 0.5, color="gray", linewidth=0.5)

    # Label each cell with its k value
    for r in range(r_count):
        for c in range(c_count):
            k = grid[r][c]
            if k > 0:
                text_color = "white" if np.mean(color_grid[r, c, :3]) < 0.5 else "black"
                ax.text(c, r, str(k), ha="center", va="center", fontsize=8, color=text_color)

    ax.set_title(title)
    plt.setp(ax.get_xticklabels(), rotation=0)


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    grid_str = parse_grid(input_path)
    r_count = len(grid_str)
    c_count = len(grid_str[0])

    solved_n = None
    status = cp_model.UNKNOWN
    collector = None

    for candidate_n in (17, 16):
        model, x = build_model(grid_str, n=candidate_n)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 180
        solver.parameters.num_search_workers = 8

        collector = SolutionCollector(x, r_count, c_count, candidate_n)
        status = solver.solve(model, solution_callback=collector)

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            solved_n = candidate_n
            break

    if solved_n is None or not collector or not collector.solutions:
        print("No solution found for N=16 or N=17.")
        return

    n_solutions = len(collector.solutions)
    print(f"Found {n_solutions} solution(s).")

    # Plot each solution (or a subset if many)
    if n_solutions == 1:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        visualize_solution(collector.solutions[0], solved_n, title="Final solution", ax=ax)
    elif n_solutions <= 4:
        ncols = min(2, n_solutions)
        nrows = (n_solutions + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=(7 * ncols, 5 * nrows))
        axes_flat = np.array(axes).flatten()
        for i, sol in enumerate(collector.solutions):
            visualize_solution(
                sol,
                solved_n,
                title=f"Solution {i + 1} of {n_solutions}",
                ax=axes_flat[i],
            )
        for j in range(n_solutions, len(axes_flat)):
            axes_flat[j].set_visible(False)
    else:
        # Many solutions: show first, middle, and last
        indices = [0, n_solutions // 2, n_solutions - 1]
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        for idx, ax in zip(indices, axes):
            visualize_solution(
                collector.solutions[idx],
                solved_n,
                title=f"Solution {idx + 1} of {n_solutions}",
                ax=ax,
            )

    plt.tight_layout()
    plt.savefig(Path(__file__).with_name("subtiles_solution.png"), dpi=120, bbox_inches="tight")
    print("Saved subtiles_solution.png")
    plt.show()


if __name__ == "__main__":
    main()
