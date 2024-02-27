import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def visualize_path(maze, path, start, goal, visited_nodes, expanded_nodes, file_name, search_type):
    maze_array = np.array(maze)
    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    # Drawing the maze
    for y in range(maze_array.shape[0]):
        for x in range(maze_array.shape[1]):
            color = 'white' if maze_array[y, x] else 'black'
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

    # Drawing visited nodes in dark blue
    for x, y in visited_nodes:
        if (x, y) not in path and (x, y) != start and (x, y) != goal:  # Avoid overwriting start, goal, and path
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color='darkblue'))

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

    # Adding legend outside the grid to the right
    legend_elements = [
        Patch(facecolor='lime', edgecolor='lime', label='Start'),
        Patch(facecolor='red', edgecolor='red', label='Goal'),
        Patch(facecolor='skyblue', edgecolor='skyblue', label='Path'),
        Patch(facecolor='darkblue', edgecolor='darkblue', label='Explored')]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

    # Adjust subplot to make room for the legend
    plt.subplots_adjust(right=0.85)
    
    # Count of expanded cells
    expanded_cells_count = len(visited_nodes)
    
    # Display count of expanded cells
    plt.figtext(0.5, 0.01, f'Expanded Cells Count: {expanded_nodes}', ha="center", fontsize=12)

    # Displaying the title with file name and search type
    title_text = f"{file_name.split('/')[2]} - {search_type}"
    plt.title(title_text, fontsize=14, pad=20)

    plt.show()

def visualize_path_adaptive(maze, path, start, goal, visited_nodes, expanded_nodes, file_name, search_type, adaptive_search_num):
    maze_array = np.array(maze)
    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    # Drawing the maze
    for y in range(maze_array.shape[0]):
        for x in range(maze_array.shape[1]):
            color = 'white' if maze_array[y, x] else 'black'
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

    # Drawing visited nodes in dark blue
    for x, y in visited_nodes:
        if (x, y) not in path and (x, y) != start and (x, y) != goal:  # Avoid overwriting start, goal, and path
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color='darkblue'))

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

    # Adding legend outside the grid to the right
    legend_elements = [
        Patch(facecolor='lime', edgecolor='lime', label='Start'),
        Patch(facecolor='red', edgecolor='red', label='Goal'),
        Patch(facecolor='skyblue', edgecolor='skyblue', label='Path'),
        Patch(facecolor='darkblue', edgecolor='darkblue', label='Explored')]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

    # Adjust subplot to make room for the legend
    plt.subplots_adjust(right=0.85)
    
    # Display count of expanded cells
    plt.figtext(0.5, 0.01, f'Expanded Cells Count: {expanded_nodes}', ha="center", fontsize=12)

    # Displaying the title with file name and search type
    title_text = f"{file_name.split('/')[2]} - {search_type}"
    plt.title(title_text, fontsize=14, pad=20)
    
    # Display count of expanded cells
    plt.savefig(f"{file_name.split('/')[2]}_adaptive_search_{adaptive_search_num}.png", bbox_inches='tight')
    plt.close()  # Close the figure to free up memory