# Oral-Defense Notes

1. **What problem does the project solve?** It finds a route through a rectangular grid from a start cell to a goal while avoiding obstacles.
2. **What is a search algorithm?** It systematically explores possible states to find one that satisfies a goal condition.
3. **What is a state in this maze?** A coordinate `(row, column)` for a traversable cell.
4. **What are the initial and goal states?** They are the selected start and destination coordinates.
5. **What actions can the agent perform?** Move one cell up, down, left, or right when the destination cell is in bounds and traversable.
6. **What is the cost of one movement?** One unit. The total path cost is the number of moves.
7. **What is BFS?** Breadth-First Search explores states in layers, in order of their number of moves from the start.
8. **Why does BFS use a FIFO queue?** First-in, first-out ordering processes states at smaller depths before states at larger depths.
9. **Why track discovered states?** It prevents revisiting cells and ensures each cell is enqueued at most once. This implementation marks a cell discovered when it is enqueued.
10. **How is the path reconstructed?** A predecessor map stores each cell's parent. Starting at the goal, the program follows those links back to the start and reverses the coordinates.
11. **Why was BFS selected?** The maze has a finite grid and equal movement costs. BFS is straightforward for this problem and finds a shortest route in number of moves.
12. **Is BFS complete here?** Yes. The grid has finitely many cells, and discovered tracking prevents repeated enqueuing. BFS will eventually find a reachable goal or exhaust all reachable cells and report failure.
13. **Is BFS optimal here?** Yes. Every legal move costs one, so a route with the fewest moves also has the lowest total cost. BFS processes cells in increasing move distance from the start.
14. **What happens when no path exists?** The queue empties and the result has `found=False`, an empty path, and `path_cost=None`.
15. **What does explored-node count mean?** It counts cells removed from the queue and processed, in order. It includes the goal when reached; if no route exists, it counts every reachable cell processed before the queue empties.
16. **How is path cost calculated?** It is `len(path) - 1`, the number of moves between path cells. It is zero when start and goal are identical, and `None` when no route exists.
17. **What are the complexities?** For `R` rows and `C` columns, time is `O(RC)` and worst-case auxiliary space is `O(RC)`. Each cell is processed at most once and has at most four neighbors.
18. **What are the limitations?** The GUI uses a fixed-size grid, supports four directions, and assumes all moves have equal cost. It does not animate search or model diagonal or weighted movement.
19. **Why might BFS be unsuitable for different movement costs?** BFS orders by number of edges rather than total cost. With unequal costs, fewer moves can be more expensive; a cost-aware algorithm such as uniform-cost search is needed.
