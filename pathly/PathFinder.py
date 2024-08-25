from typing import Tuple, List, Optional, Dict
import numpy as np
from collections import deque

def is_valid(grid, coordinates):
    x, y = coordinates
    return 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]

def is_safe(grid, coordinates, fire):
    x, y = coordinates
    if not is_valid(grid, coordinates) or grid[x, y] == 0 or fire[x, y] == 1:
        return False
    return True

def _get_path(parent, goal):
    path = []
    while goal:
        path.append(goal)
        goal = parent.get(goal, None)
    return path[::-1]

def _bfs(grid=None, goal_nodes=None, entry=(3, 25), fire=None):
    q = deque([entry])
    q.append(entry)
    visited = set([entry])
    parent = {}
    goal = None
    while q:
        current = q.popleft()
        if current in goal_nodes:
            goal = current
            break
        children = [
                    (current[0], current[1]-1), (current[0], current[1]+1), 
                    (current[0]-1, current[1]), (current[0]+1, current[1]), 
                    (current[0]-1, current[1]-1), (current[0]+1, current[1]+1), 
                    (current[0]-1, current[1]+1), (current[0]+1, current[1]-1)
                    ]
        for child in children:
            if is_safe(grid, child):
                if child not in visited:
                    q.append(child)
                    visited.append(child)
                    parent[child] = current
    if goal is None:
        return (parent, None)
    return (parent, goal)

def path_finder(grid: np.ndarray, goal_nodes: List[Tuple[int, int]], entry: Tuple[int, int], fire: Optional[np.ndarray] = None) -> List[Tuple[int, int]]:
    if grid is None or goal_nodes is None:
        raise ValueError('Grid and goal nodes are required')
    if fire is None:
        fire = np.zeros(grid.shape, dtype=int)
    if not is_safe(grid, entry, fire):
        raise ValueError('Entry point is not safe')
    
    parent, goal = _bfs(grid, goal_nodes, entry, fire)
    if goal is None:
        raise Exception('No path found')
    
    return _get_path(parent, goal)
