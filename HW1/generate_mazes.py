# generate_mazes.py
from grid_world import GridWorld
import os
import random

def save_maze_to_file(maze, filename):
    with open(filename, 'w') as file:
        for row in range(maze.rows):
            for col in range(maze.cols):
                file.write('O' if maze.path[row][col] else 'X')
            file.write('\n')

def generate_and_save_mazes(num_mazes, rows, cols, directory='HW1/mazes'): #again, we are assuming you are in CS440 folder directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(num_mazes):
        random.seed(i)
        maze = GridWorld(rows, cols)
        maze.create_maze()
        filename = os.path.join(directory, f'maze{i}.txt')
        save_maze_to_file(maze, filename)
        print(f'Maze {i} saved to {filename}')

if __name__ == "__main__":
    generate_and_save_mazes(50, 101, 101)
