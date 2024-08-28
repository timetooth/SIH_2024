'''
The module contains the functions to simulate the spread of fire 
in a grid using cellular automata algorithm based on a heuristics based probabalistic model.

The model is based on the following assumptions:
1. The probability of a cell catching fire is based on the number of active neighbours and their distance.
2. The probability of a cell catching fire is based on the time to ignition of the cell.
'''
import numpy as np
import random
import matplotlib.pyplot as plt

max_tti = 500
def initialize_grid(ignite_cell, shape=(15,26)):
    start_x, start_y = ignite_cell
    grid = np.zeros(shape)
    # not-burning-0, burning-1, burnt-2, protected-3, barrier-4 for future implementation
    tti = np.random.randint(1, max_tti, size=shape)
    grid[start_x][start_y] = 1
    return grid, tti

def is_valid(grid, coordinates):
    x, y = coordinates[0], coordinates[1]
    if x < 0 or x >= grid.shape[0] or y < 0 or y >= grid.shape[1]:
        return False
    return True

def neighbour_factor(grid, coordinates):
    x, y = coordinates[0], coordinates[1]
    nearest_active = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_valid(grid, (x+i, y+j)) and grid[x+i][y+j] == 1:
                nearest_active += 1
    farther_active = 0
    for i in range(-2, 3):
        for j in range(-2, 3):
            if is_valid(grid, (x+i, y+j)) and grid[x+i][y+j] == 1:
                if abs(i) < 2 and abs(j) < 2: nearest_active += 1
                else: farther_active += 1
    return (nearest_active, farther_active)

def spread_probability(grid, coordinates, tti, neighbour_factors, alpha=1, beta=0.5):
    '''
    Calculates the probability of the given cell catching fire
    alpha: hyperparameter for final scaling
    beta: hyperparameter, weight for farther active cells
    equation => p = 1 - e^(-alpha*(1 + near + beta*far)*tti)
    '''
    x, y = coordinates
    near, far = neighbour_factors
    # standardize and scale the near and far neighbours
    near = near/8
    far = beta*(far/16)
    tti_val = tti[x][y]/max_tti
    prob = 1 - np.exp(-alpha*(1 + near + far)*tti_val)
    return prob

def update_grid(grid, tti, alpha=1, beta=0.5, gamma=0.1):
    updated = grid.copy()
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        child_x, child_y = i+dx, j+dy
                        if is_valid(grid, (child_x, child_y)) and grid[child_x][child_y] == 0:
                            neighbour_factors = neighbour_factor(grid, (child_x, child_y))
                            prob = spread_probability(grid, (child_x, child_y), tti, neighbour_factors, alpha, beta)
                            if random.random() < gamma*prob:
                                updated[child_x][child_y] = 1
    return updated

def visualize_grid(grid, step):
    """ Visualize the grid using Matplotlib. """
    plt.imshow(grid, cmap='binary', interpolation='nearest')
    plt.title(f'Cellular Automaton - Step {step}')
    plt.colorbar()
    plt.pause(0.1)

def show_simulation(ignite_cell, shape, alpha=1, beta=0.5, gamma=0.1, steps=50):
    start_x, start_y = ignite_cell
    grid, tti = initialize_grid(ignite_cell, shape=shape)
    visualize_grid(grid, 0)
    for step in range(1, steps):
        grid = update_grid(grid, tti, alpha, beta, gamma)
        visualize_grid(grid, step)
    plt.show()

def simulate_fire(ignite_cell, shape, alpha=1, beta=0.5, gamma=0.1, steps=50):
    '''
    Each grid acts a key frame for the simulation
    ignite_cell: tuple of x, y coordinates of the cell to ignite
    shape: tuple of rows and columns of the grid
    alpha: hyperparameter for final scaling in spread_probability
    beta: hyperparameter, weight for farther active cells in spread_probability
    gamma: speed factor (resolution) for the spread of fire
    steps: number of steps to simulate/frames to generate
    Returns: an array of size steps containing the situation of gid at each step
    '''
    key_frames = []
    grid, tti = initialize_grid(ignite_cell, shape=shape)
    for _ in range(1, steps):
        grid = update_grid(grid, tti, alpha, beta, gamma)
        key_frames.append(grid.copy())
    return key_frames