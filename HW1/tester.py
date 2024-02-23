import random
import matplotlib.pyplot as plt
import numpy as np
from generate_mazes import generate_and_save_mazes
from maze_driver import display_all_mazes
from a_star import aStar
from path_visualizer import visualize_path



def get_valid_positions(maze):
    valid_positions = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell]
    return valid_positions

def read_maze_from_file(file_path):
    maze = []
    expected_row_length = 101  # Expected number of characters per row
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if len(stripped_line) != expected_row_length:
                raise ValueError(f"Row length is {len(stripped_line)}, expected {expected_row_length}")
            maze.append([True if char == 'O' else False for char in stripped_line])
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
    maze = read_maze_from_file(maze_file)  # This returns the maze as a list of lists (True/False values)
    start, goal = choose_random_positions(maze)  # This should return ((start_x, start_y), (goal_x, goal_y))

    # Instantiate a_star_solver with correct parameters
    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1])
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
