import matplotlib.pyplot as plt
import numpy as np
import os

def read_grid_from_file(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            grid.append([1 if char == 'O' else 0 for char in line.strip()])
    return np.array(grid)

def display_maze(file_path):
    grid = read_grid_from_file(file_path)
    plt.imshow(grid, cmap='gray', interpolation='nearest')
    #make title the maze plus number example: Maze 1
    plt.title(file_path.split('/')[2], fontsize=8)
    plt.axis('off')  # Hide axes ticks
    plt.show()

def display_all_mazes(directory, num_mazes=50, rows=5, cols=10):
    fig, axs = plt.subplots(rows, cols, figsize=(20, 20))
    for i in range(num_mazes):
        file_path = os.path.join(directory, f'maze{i}.txt')
        grid = read_grid_from_file(file_path)
        ax = axs[i // cols, i % cols]
        ax.imshow(grid, cmap='gray', interpolation='nearest')
        ax.set_title(f'Maze {i}', fontsize=8)
        ax.axis('off')  # Hide axes ticks
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    directory = 'HW1/mazes'   # assuming you are in CS440 folder directory
    display_all_mazes(directory)
