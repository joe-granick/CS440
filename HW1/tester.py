import argparse
import sys
import random
import matplotlib.pyplot as plt
import numpy as np
from generate_mazes import generate_and_save_mazes
from maze_driver import display_all_mazes
from a_star import aStar
from grid_world import GridWorld


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



def get_valid_positions(maze):
    valid_positions = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell]
    return valid_positions

def read_maze_from_file(file_path):
    maze = []
    with open(file_path, 'r') as file:
        for line in file:
            maze.append([True if char == 'O' else False for char in line.strip()])
    return maze

def choose_random_positions(maze):
    valid_positions = get_valid_positions(maze)
    start = random.choice(valid_positions)
    goal = random.choice(valid_positions)
    while start == goal:  # Ensure start and goal are not the same
        goal = random.choice(valid_positions)
    return start, goal

def generate_mazes():
    # Your maze generation logic here
    print("Generating 50 mazes...")
    generate_and_save_mazes(50, 101, 101, 'HW1/mazes')


def view_mazes():
    # Your maze viewing logic here
    print("Viewing all 50 mazes...")
    display_all_mazes('HW1/mazes')


def get_maze_file():
    while True:
        maze_number = input("Enter the maze number to use (0-49): ")
        try:
            maze_number = int(maze_number)
            if 0 <= maze_number <= 49:
                return f"maze{maze_number}.txt"  # Construct the file name based on the number
            else:
                print("Invalid maze number. Please enter a number between 0 and 49.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def run_a_star_forward(maze_file):
    print(f"Running A* Forward on {maze_file}...")
    maze = read_maze_from_file(maze_file)
    start, goal = choose_random_positions(maze)

    a_star_solver = aStar(maze_file, *start, *goal)
    path = a_star_solver.a_star_fwd()

    if path:
        visualize_path(maze, path, start, goal)
    else:
        print("No path found.")

def run_a_star_backward(maze_file):
    print(f"Running A* backward on {maze_file}...")
    maze = read_maze_from_file(maze_file)
    start, goal = choose_random_positions(maze)

    a_star_solver = aStar(maze_file, *start, *goal)
    path = a_star_solver.a_star_bwd()

    if path:
        visualize_path(maze, path, start, goal)
    else:
        print("No path found.")


def main():
    while True:
        print("\nPlease select an option:")
        print("1 - Generate 50 mazes")
        print("2 - View all 50 mazes")
        print("3 - Run A* Forward")
        print("4 - Run A* Backward")
        print("5 - Exit")

        option = input("Enter your choice: ")
        maze_file_path = None  # Initialize maze_file_path to None (or an appropriate default)

        if option in ["3", "4"]:
            maze_file = get_maze_file()  # This function should ask for input and return the filename
            maze_file_path = f"HW1/mazes/{maze_file}"  # Construct the full path

        if option == "1":
            generate_mazes()
        elif option == "2":
            view_mazes()
        elif option == "3" and maze_file_path:
            run_a_star_forward(maze_file_path)
        elif option == "4" and maze_file_path:
            run_a_star_backward(maze_file_path)
        elif option == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose a valid option (1-5).")


if __name__ == "__main__":
    main()
