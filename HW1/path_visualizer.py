import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def visualize_path(maze, path, start, goal):
    maze_array = np.array(maze)
    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    # Drawing the maze
    for y in range(maze_array.shape[0]):
        for x in range(maze_array.shape[1]):
            color = 'white' if maze_array[y, x] else 'black'
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

    # Drawing the path
    for x, y in path:
        ax.add_patch(plt.Rectangle((x, y), 1, 1, color='skyblue'))

    # Drawing start and goal positions
    ax.add_patch(plt.Rectangle(start, 1, 1, color='lime', fill=True))
    ax.add_patch(plt.Rectangle(goal, 1, 1, color='red', fill=True))

    # Adjusting plot limits and aspect ratio
    plt.xlim(0, maze_array.shape[1])
    plt.ylim(0, maze_array.shape[0])
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')

    # Adding legend
    legend_elements = [Patch(facecolor='lime', edgecolor='lime', label='Start'),
                       Patch(facecolor='red', edgecolor='red', label='Goal'),
                       Patch(facecolor='skyblue', edgecolor='skyblue', label='Path')]
    plt.legend(handles=legend_elements, loc='upper left')

    plt.show()
