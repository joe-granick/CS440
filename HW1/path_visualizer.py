import numpy as np
import matplotlib.pyplot as plt

def visualize_path(maze, path, start, goal):
    maze_array = np.array(maze)
    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    for y in range(maze_array.shape[0]):
        for x in range(maze_array.shape[1]):
            color = 'white' if maze_array[y, x] else 'black'
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

    for x, y in path:
        ax.add_patch(plt.Rectangle((x, y), 1, 1, color='skyblue'))

    ax.add_patch(plt.Rectangle(start, 1, 1, color='lime', fill=True))
    ax.add_patch(plt.Rectangle(goal, 1, 1, color='red', fill=True))

    plt.xlim(0, maze_array.shape[1])
    plt.ylim(0, maze_array.shape[0])
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()