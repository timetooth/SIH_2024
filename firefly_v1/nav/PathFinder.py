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
            if is_safe(grid, child, fire):
                if child not in visited:
                    q.append(child)
                    visited.add(child)
                    parent[child] = current
    if goal is None:
        return (parent, None)
    return (parent, goal)

def path_finder(grid, goal_nodes, entry, fire = None):
    '''
    This function is used to find the path from the entry point to the nearest goal node
    grid: 2D list of integers, where 0 is a wall, 1 is a path
    goal_nodes:2D list of goal nodes in the grid
    entry: list of entry point coordinates [x, y]
    fire: 2D list of fire in the grid, where 1 is fire and 0 is no fire
    '''
    grid = np.array(grid)
    entry = tuple(entry)
    goal_nodes = [tuple(node) for node in goal_nodes]
    fire = np.array(fire) if fire is not None else None
    if grid is None or goal_nodes is None:
        raise ValueError('Grid and goal nodes are required')
    if fire is None:
        fire = np.zeros(grid.shape, dtype=int)
    if not is_safe(grid, entry, fire):
        raise ValueError('Entry point is not safe')
    
    parent, goal = _bfs(grid, goal_nodes, entry, fire)
    if goal is None:
        return []
    
    return _get_path(parent, goal)

def map_handler(grid):
    grid = np.array(grid)
    fire_exits, med_kits, extinguishers = [], [], []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 2:
                fire_exits.append([i, j])
                grid[i, j] = 1
            elif grid[i, j] == 3:
                med_kits.append([i, j])
                grid[i, j] = 1
            elif grid[i, j] == 4:
                extinguishers.append([i, j])
                grid[i, j] = 1
            elif grid[i, j] == -1:
                grid[i, j] = 0
    return grid, fire_exits, med_kits, extinguishers