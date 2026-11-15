# Maze Solver Using Breadth-First Search (BFS)

**Course:** Fundamentals of Artificial Intelligence (CF321)

## Project overview

This project is a small desktop application that solves a finite, rectangular maze with Breadth-First Search (BFS). It combines a pure, independently testable search algorithm with a Tkinter grid editor that visualizes the cells actually processed and the route returned by the algorithm.

## Problem statement

Given a two-dimensional grid of traversable cells and obstacles, find a route from a specified start to a specified goal. Movement is limited to one cell up, down, left, or right. Diagonal moves are prohibited, and every move costs one.

## Project objectives

- Represent a navigation problem as states, actions, transitions, and a goal test.
- Implement FIFO queue-based BFS and predecessor-based path reconstruction.
- Demonstrate shortest-path behavior on a unit-cost grid.
- Validate results with standard-library automated tests.

## AI problem formulation

- **State space:** All coordinates `(row, column)` of traversable cells.
- **Initial state:** The user-selected start coordinate.
- **Goal state:** The user-selected destination coordinate.
- **Available actions:** Move up, down, left, or right by one cell.
- **Transition model:** An action reaches the adjacent in-bounds traversable cell; actions that leave the grid or enter a wall are illegal.
- **Step cost:** Exactly 1 for each legal move.
- **Goal test:** The current coordinate equals the goal coordinate.

## Why BFS was selected

BFS expands states in increasing number of moves from the start. Since every legal movement has equal cost, the first discovered goal has a minimum-move route. Ordinary BFS does not guarantee a lowest-cost route when edges have arbitrary unequal costs.

## How BFS works in this project

`solve_maze` validates the input, enqueues the start in a `collections.deque`, and marks cells discovered when they are enqueued. It removes and processes cells in FIFO order, examining neighbors deterministically in up, down, left, right order. The predecessor map records where each discovered cell came from. Each traversable coordinate enters the queue at most once.

When the goal is removed from the queue and processed, the algorithm follows predecessor links from goal to start and reverses that list. If the queue empties first, it returns an unsuccessful result with no path.

`SearchResult.explored_nodes` records cells removed from the queue and processed, in order. It includes the goal when reached. `explored_count` is the length of this list. For an unreachable goal it counts all cells processed before the queue empties. `path_cost` is the number of moves (`len(path) - 1`), or `None` if no path exists. Start equal to goal produces one path coordinate, zero cost, and one explored node.

## Features

- Interactive 12-by-16 grid with start, goal, wall editing, explored-cell and shortest-path colors.
- Start and goal selection, wall toggling, example loading, wall clearing, reset, and BFS solve controls.
- Clear validation messages and stale-result clearing after maze edits.
- Pure BFS solver with deterministic exploration and explicit invalid-input errors.
- `unittest` coverage without a display requirement.

## Technology requirements

Python 3.10 or later and its standard library only. The interface uses Tkinter and ttk, which are normally included with Python distributions; a graphical display is required to open the application. No third-party packages or installation steps are needed.

## Project structure

```text
maze-solver-bfs/
├── main.py
├── maze_solver/
│   ├── __init__.py
│   ├── solver.py
│   └── gui.py
├── tests/
│   └── test_solver.py
├── README.md
├── DEFENSE_NOTES.md
└── .gitignore
```

## Setup and commands

Open a terminal at the project root. To launch the GUI:

```bash
python main.py
```

To run the automated tests:

```bash
python -m unittest discover -s tests -v
```

To compile Python files:

```bash
python -m compileall -q .
```

## Using the interface

1. **Solve with BFS** runs the implemented solver on the current grid and displays success or failure, move cost, processed-node count, and the returned route.
2. **Select Start** then click a traversable grid cell to move the start.
3. **Select Goal** then click a traversable grid cell to move the goal.
4. **Toggle Wall** then click a grid cell to add or remove an obstacle. Start and goal cells are protected.
5. **Load Example Maze** loads a predefined maze with barriers and openings. The route is computed by BFS when solved; it is not stored in the example.
6. **Clear Walls** makes every cell traversable and preserves the current start and goal.
7. **Reset** restores the documented example maze and default positions.

Any successful maze edit clears prior overlays and metrics. The legend maps empty cells, walls, start, goal, explored cells, and final path to distinct colors. Start and goal markers remain visible over the search result.

## Example scenarios

- The initial example is solvable and routes around barriers. Exact route details depend on the documented deterministic neighbor order.
- On an open grid, BFS finds a Manhattan-shortest route.
- A complete wall barrier can make the goal unreachable; the application reports failure and processed-node count without showing a path.
- Selecting the same traversable cell for start and goal returns a zero-move route.

## Complexity

For an `R` by `C` grid, at most `RC` cells are discovered and processed, each with at most four neighbors. Time complexity is `O(RC)` and auxiliary space complexity is `O(RC)` in the worst case, including the queue, discovered set, predecessor map, and result data.

## Assumptions and limitations

The grid must be non-empty, rectangular, and contain integer `0` (traversable) or `1` (obstacle) values. Start and goal must be in bounds and traversable. Motion is four-directional and all moves have equal cost. The GUI uses a fixed grid size and presents completed search results statically; it does not animate queue processing or support weighted movement.

## Testing and submission

The tests cover valid and minimum-length paths, obstacle detours, unreachable goals and their exploration count, start equal to goal, blocked and invalid inputs, a single cell, boundaries, and deterministic output. Run the commands above from the repository root before submission. This repository does not claim external evaluation or certification.
