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

def _path_shortner(path):
    if len(path) <= 3:
        return path
    i = 2
    while i < len(path)-1:
        while i < len(path)-1 and path[i][0] == path[i-2][0] and path[i][0] == path[i-1][0]:
            path.pop(i-1)
        while i < len(path)-1 and path[i][1] == path[i-2][1] and path[i][1] == path[i-1][1]:
            path.pop(i-1)
        i += 1
    return path

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
    
    path = _get_path(parent, goal)
    path = _path_shortner(path)
    return [calculate_lat_lon(coordinates, grid.shape) for coordinates in path]

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


# rectangle = {'bottom_left': (77.1846478279088,28.622942618204192),'top_left': (77.1846478279088,28.631081792092175),'top_right': (77.19316906505497,28.631081792092175),'bottom_right': (77.19316906505497,28.622942618204192)}

top_left = [28.631081792092175,77.1846478279088]
bottom_right = [28.622942618204192, 77.19316906505497]

def calculate_lat_lon(coordinates, size):
    i, j = coordinates
    rows, cols = size
    delta_long = (bottom_right[1] - top_left[1])/cols
    delta_lat = (top_left[0] - bottom_right[0])/rows

    lat = top_left[0] - i*delta_lat
    lon = top_left[1] + j*delta_long
    
    return [lon, lat]

# def calculate_lat_lon(coordinates, size):
#     i, j = coordinates
#     rows, cols = size
#     lat = top_left[1] - ((top_left[1] - bottom_right[1]) * i / rows)
#     lon = top_left[0] + ((bottom_right[0] - top_left[0]) * j / cols)
#     return [lon, lat]