import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def overlay_gen(grid=None, color=[0,0,0], grid_shape=[15,26]):
    """
    create a binary rgba image from a 2D grid
    """
    if grid is None:
        grid = np.random.randint(-1, 1, grid_shape).astype(np.uint8)*255
    rgba_image = np.zeros((grid.shape[0], grid.shape[1], 4))
    rgba_image[grid == 1] = [color[0], color[1], color[2], 1] 
    rgba_image[grid == 0] = [0, 0, 0, 0]
    return rgba_image

def overlay(image = None, grid=None, grid_shape=[15,26], alpha=0.3, figsize=(7,13), color=[0,0,0]):
    """
    overlay the binary grid on the image
    """
    if image is None:
        image = cv.imread('./map.jpg')
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    if grid is None:
        grid = np.random.randint(-1, 1, grid_shape).astype(np.uint8)*255
    binary_image = grid.copy()
    if len(binary_image.shape) == 2:
        binary_image = overlay_gen(grid, color = color)
    plt.figure(figsize=figsize)
    plt1 = plt.imshow(image, extent=[0, grid_shape[1], grid_shape[0], 0])
    plt2 = plt.imshow(binary_image, alpha=alpha, extent=[0, grid_shape[1], grid_shape[0], 0])
    plt.yticks(np.arange(0, grid_shape[0], 1))
    plt.xticks(np.arange(0, grid_shape[1], 1))
    plt.tick_params(axis='x', top=True)
    plt.show()
    return