"""Tkinter interface for editing and solving a small grid maze."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .solver import solve_maze

ROWS = 12
COLUMNS = 16
CELL_SIZE = 38
DEFAULT_START = (1, 1)
DEFAULT_GOAL = (10, 14)


def _empty_grid() -> list[list[int]]:
    return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]


def _example_grid() -> list[list[int]]:
    grid = _empty_grid()
    # A vertical barrier with two openings forces a genuine detour.
    for row in range(1, 10):
        if row not in (4, 8):
            grid[row][7] = 1
    for column in range(2, 7):
        grid[3][column] = 1
    for column in range(8, 14):
        grid[7][column] = 1
    return grid


class MazeSolverApp:
    """Interactive maze editor and visualization of the solver's result."""

    COLORS = {
        "empty": "#f4f7fb", "wall": "#334155", "start": "#16a36a",
        "goal": "#e24b58", "explored": "#8ecae6", "path": "#f5c451",
        "grid": "#cbd5e1",
    }

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Maze Solver Using BFS")
        self.root.configure(bg="#eef2f7")
        self.root.resizable(False, False)
        self.grid = _example_grid()
        self.start = DEFAULT_START
        self.goal = DEFAULT_GOAL
        self.mode: str | None = None
        self.result = None
        self._build_ui()
        self._draw_grid()

    def _build_ui(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#eef2f7")
        style.configure("TLabel", background="#eef2f7", foreground="#172033", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#14213d")
        style.configure("Sub.TLabel", foreground="#526174")
        style.configure("TButton", font=("Segoe UI", 10), padding=(9, 7))
        style.configure("Accent.TButton", background="#2357a6", foreground="white")

        outer = ttk.Frame(self.root, padding=20)
        outer.grid(row=0, column=0)
        ttk.Label(outer, text="Maze Solver Using BFS", style="Title.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(outer, text="Edit a grid and watch breadth-first search find a shortest route.", style="Sub.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(3, 15))

        self.canvas = tk.Canvas(outer, width=COLUMNS * CELL_SIZE, height=ROWS * CELL_SIZE,
                                bg="white", highlightthickness=1, highlightbackground="#cbd5e1")
        self.canvas.grid(row=2, column=0, rowspan=5, sticky="n", padx=(0, 20))
        self.canvas.bind("<Button-1>", self._on_grid_click)

        panel = ttk.Frame(outer, padding=(0, 0, 0, 0))
        panel.grid(row=2, column=1, sticky="n")
        ttk.Label(panel, text="CONTROLS", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 6))
        ttk.Button(panel, text="Solve with BFS", style="Accent.TButton", command=self.solve).grid(row=1, column=0, sticky="ew", pady=3)
        ttk.Button(panel, text="Select Start", command=lambda: self._set_mode("start")).grid(row=2, column=0, sticky="ew", pady=3)
        ttk.Button(panel, text="Select Goal", command=lambda: self._set_mode("goal")).grid(row=3, column=0, sticky="ew", pady=3)
        ttk.Button(panel, text="Toggle Wall", command=lambda: self._set_mode("wall")).grid(row=4, column=0, sticky="ew", pady=3)
        ttk.Button(panel, text="Load Example Maze", command=self.load_example).grid(row=5, column=0, sticky="ew", pady=(12, 3))
        ttk.Button(panel, text="Clear Walls", command=self.clear_walls).grid(row=6, column=0, sticky="ew", pady=3)
        ttk.Button(panel, text="Reset", command=self.reset).grid(row=7, column=0, sticky="ew", pady=3)

        ttk.Separator(panel).grid(row=8, column=0, sticky="ew", pady=12)
        ttk.Label(panel, text="RESULTS", font=("Segoe UI", 10, "bold")).grid(row=9, column=0, sticky="w")
        self.result_text = tk.StringVar(value="Not solved yet")
        ttk.Label(panel, textvariable=self.result_text, wraplength=225, justify="left").grid(row=10, column=0, sticky="w", pady=(7, 10))
        ttk.Label(panel, text="LEGEND", font=("Segoe UI", 10, "bold")).grid(row=11, column=0, sticky="w", pady=(3, 5))
        legend = [("Empty", "empty"), ("Wall", "wall"), ("Start", "start"), ("Goal", "goal"), ("Explored", "explored"), ("Path", "path")]
        for i, (label, color_key) in enumerate(legend):
            row, col = divmod(i, 2)
            item = ttk.Frame(panel)
            item.grid(row=12 + row, column=col, sticky="w", padx=(0, 8), pady=2)
            tk.Label(item, bg=self.COLORS[color_key], width=2, relief="solid", bd=1).pack(side="left", padx=(0, 5))
            ttk.Label(item, text=label).pack(side="left")

        self.status = tk.StringVar(value="Ready. Choose a control, then click a cell to edit the maze.")
        ttk.Label(outer, textvariable=self.status, style="Sub.TLabel", wraplength=900).grid(row=7, column=0, columnspan=2, sticky="w", pady=(13, 0))

    def _draw_grid(self) -> None:
        self.canvas.delete("all")
        explored = set(self.result["explored_nodes"]) if self.result else set()
        path = set(self.result["path"]) if self.result and self.result["found"] else set()
        for row in range(ROWS):
            for column in range(COLUMNS):
                cell = (row, column)
                color = self.COLORS["wall"] if self.grid[row][column] else self.COLORS["empty"]
                if cell in explored:
                    color = self.COLORS["explored"]
                if cell in path:
                    color = self.COLORS["path"]
                if cell == self.start:
                    color = self.COLORS["start"]
                elif cell == self.goal:
                    color = self.COLORS["goal"]
                x1, y1 = column * CELL_SIZE, row * CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x1 + CELL_SIZE, y1 + CELL_SIZE,
                                             fill=color, outline=self.COLORS["grid"], width=1)
                if cell == self.start:
                    self.canvas.create_text(x1 + CELL_SIZE / 2, y1 + CELL_SIZE / 2, text="S", fill="white", font=("Segoe UI", 12, "bold"))
                elif cell == self.goal:
                    self.canvas.create_text(x1 + CELL_SIZE / 2, y1 + CELL_SIZE / 2, text="G", fill="white", font=("Segoe UI", 12, "bold"))

    def _clear_result(self) -> None:
        self.result = None
        self.result_text.set("Not solved yet")
        self._draw_grid()

    def _set_mode(self, mode: str) -> None:
        self.mode = mode
        names = {"start": "start", "goal": "goal", "wall": "wall"}
        self.status.set(f"Select {names[mode]}: click a cell in the maze.")

    def _on_grid_click(self, event: tk.Event) -> None:
        column, row = int(event.x // CELL_SIZE), int(event.y // CELL_SIZE)
        cell = (row, column)
        if not (0 <= row < ROWS and 0 <= column < COLUMNS):
            return
        if self.mode is None:
            self.status.set("Choose Select Start, Select Goal, or Toggle Wall before clicking the grid.")
            return
        mode, self.mode = self.mode, None
        if mode == "wall":
            if cell == self.start or cell == self.goal:
                self.status.set("A wall cannot replace the start or goal cell.")
                return
            self.grid[row][column] = 0 if self.grid[row][column] else 1
            self._clear_result()
            self.status.set("Wall updated. Previous search results were cleared.")
        elif self.grid[row][column] == 1:
            self.status.set("Start and goal must be placed on traversable cells.")
        elif mode == "start":
            self.start = cell
            self._clear_result()
            self.status.set(f"Start moved to {cell}. Previous search results were cleared.")
        else:
            self.goal = cell
            self._clear_result()
            self.status.set(f"Goal moved to {cell}. Previous search results were cleared.")

    def solve(self) -> None:
        try:
            result = solve_maze(self.grid, self.start, self.goal)
        except ValueError as error:
            self._clear_result()
            self.status.set(f"Cannot solve this maze: {error}")
            return
        self.result = result
        if result["found"]:
            self.result_text.set(
                f"Goal reached\nPath cost: {result['path_cost']} moves\n"
                f"Explored nodes: {result['explored_count']}\nPath: {result['path']}"
            )
            self.status.set("BFS found a shortest path. Gold cells show the route; blue cells were processed.")
        else:
            self.result_text.set(
                f"Goal unreachable\nPath cost: None\nExplored nodes: {result['explored_count']}"
            )
            self.status.set("No route exists from start to goal in the current maze.")
        self._draw_grid()

    def load_example(self) -> None:
        self.grid = _example_grid()
        self.start, self.goal = DEFAULT_START, DEFAULT_GOAL
        self._clear_result()
        self.status.set("Example maze loaded. Select Solve with BFS to find its route.")

    def clear_walls(self) -> None:
        self.grid = _empty_grid()
        self._clear_result()
        self.status.set("All walls cleared. Start and goal positions were preserved.")

    def reset(self) -> None:
        self.grid = _example_grid()
        self.start, self.goal = DEFAULT_START, DEFAULT_GOAL
        self._clear_result()
        self.status.set("Reset to the example maze and default start and goal positions.")

    def run(self) -> None:
        self.root.mainloop()
