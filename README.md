# Maze-Solver-BFS
AI maze solving project using Breadth-First Search (BFS) - CF321

## 1. Project Overview

Maze Solver is a Python application that uses the **Breadth-First Search (BFS)** algorithm to find the shortest path between a starting point and a goal inside a maze.

The project includes a graphical user interface (GUI) built using Tkinter, allowing users to create and solve mazes interactively.

## 2. Algorithm — Breadth-First Search (BFS)

We chose BFS because it explores nodes level by level and guarantees the shortest path when all movements have equal costs.

The algorithm uses:

- **Queue (FIFO):** Stores nodes and their paths.
- **Visited Set:** Prevents repeated exploration of nodes.
- **Explored List:** Records processed nodes.
- **Four Directions:** Up, Down, Left, and Right.

### How BFS Works

1. Start from the initial position.
2. Add the starting node and its path to the queue.
3. Remove the first node from the queue.
4. Check whether the current node is the goal.
5. Explore valid neighboring cells.
6. Add unvisited neighbors and their paths to the queue.
7. Repeat until the goal is found or the queue becomes empty.

## 3. Project Features

- Interactive maze visualization using Tkinter.
- Set start and goal positions.
- Add and remove walls.
- Find the shortest path using BFS.
- Display the final path and its cost.
- Display the number of explored nodes.
- Handle cases where no path exists.

## 4. Technologies Used

- **Python:** Main programming language.
- **Tkinter:** Graphical user interface.
- **collections.deque:** FIFO queue implementation.

## 5. How to Run

**Step 1:** Download or clone the repository.

**Step 2:** Make sure Python 3 and Tkinter are installed.

**Step 3:** Open a terminal inside the project folder.

**Step 4:** Run the following command:

```bash
python main.py
```

**Step 5:** Use the GUI to create a maze, choose the start and goal positions, and run BFS to find the shortest path.

## 6. Project Structure

```text
Maze-Solver-BFS/
│
├── main.py
├── maze_solver/
│   ├── __init__.py
│   ├── solver.py
│   └── gui.py
│
├── README.md
└── .gitignore
```

## 7. Conclusion

This project demonstrates how Breadth-First Search can solve pathfinding problems in Artificial Intelligence.

By using a FIFO queue and exploring nodes level by level, BFS finds the shortest path in a maze where each movement has the same cost.
