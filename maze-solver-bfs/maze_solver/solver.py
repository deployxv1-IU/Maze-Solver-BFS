"""Solve a maze using BFS, following the lecture's (node, path) approach."""

from collections import deque


def solve_maze(grid, start, goal):

    # 1. Check the maze
    if not grid:
        raise ValueError("Grid must contain at least one row.")

    if not grid[0]:
        raise ValueError("Grid rows must contain at least one cell.")

    rows = len(grid)
    cols = len(grid[0])

    for row in grid:
        if len(row) != cols:
            raise ValueError("Grid must be rectangular; row lengths differ.")

        for cell in row:
            if type(cell) is not int or cell not in (0, 1):
                raise ValueError("Unsupported cell value; use 0 or 1.")

    # 2. Check Start and Goal
    for position in [start, goal]:

        # Check position format
        if type(position) != tuple:
            raise ValueError("Position must be a tuple") #Check Position Format tuple or list 

        if len(position) != 2:
            raise ValueError("Position must have row and column") # Check Number of Elements  (row,col)
        
        # (row,Col)
        r = position[0]
        c = position[1]

        # Check row and column types
        if type(r) != int or type(c) != int:
            raise ValueError("Row and column must be integers")

        # Check maze boundaries
        if r < 0 or r >= rows or c < 0 or c >= cols:
            raise ValueError("Position is outside the maze")

        # Check walls
        if grid[r][c] == 1:
            raise ValueError("Position is blocked")

    # 3. BFS Initialization
    queue = deque([(start, [start])]) # Store node and path
    visited = {start}                 # Avoid repeated nodes
    explored = []                     # Store processed nodes

    # Movement directions
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    # 4. BFS Algorithm
    while queue:

        node, path = queue.popleft() # node = (start, [start] ) & path = [(start,[start] )]
        
        explored.append(node)

        # 5. Check Goal
        if node == goal:
            return {
                "found": True,
                "path": path,
                "explored_nodes": explored,
                "path_cost": len(path) - 1,
                "explored_count": len(explored)
            }

        # 6. Explore Neighbors
        for dr, dc in directions:

            r = node[0] + dr
            c = node[1] + dc

            neighbor = (r, c)

            if (0 <= r < rows and
                0 <= c < cols and
                grid[r][c] == 0 and
                neighbor not in visited):

                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    # 7. No Solution
    return {
        "found": False,
        "path": [],
        "explored_nodes": explored,
        "path_cost": None,
        "explored_count": len(explored)
    }