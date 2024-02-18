import matplotlib.pyplot as plt
import numpy as np

def read_grid_from_file(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            grid.append([1 if char == 'O' else 0 for char in line.strip()])
    return np.array(grid)

def display_grid(grid):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='gray', interpolation='nearest')
    plt.xticks([]), plt.yticks([])  # Hide x, y ticks
    plt.show()

if __name__ == "__main__":
    file_path = 'HW1/output.txt' # 'output.txt' must be in the same directory as this file
    grid = read_grid_from_file(file_path)
    display_grid(grid)
