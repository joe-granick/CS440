import random
import matplotlib.pyplot as plt
import numpy as np
from generate_mazes import generate_and_save_mazes
from maze_driver import display_all_mazes
from a_star import aStar
from path_visualizer import visualize_path



def extract_path(goal_node):
    path = []
    current = goal_node
    while current is not None:
        path.append((current.x, current.y))  
        current = current.prev  
    path.reverse()  # Reverse the path so it goes from start to goal (or goal to start)
    return path


def get_valid_positions(maze):
    valid_positions = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell]
    return valid_positions

def read_maze_from_file(file_path):
    maze = []
    expected_row_length = 101  # per assignment instructions
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
    while start == goal:  
        goal = random.choice(valid_positions)
    return start, goal

def generate_mazes():
    print("Generating 50 mazes...")
    generate_and_save_mazes(50, 101, 101, 'HW1/mazes')


def view_mazes():
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
    start, goal = choose_random_positions(maze)  #  return ((start_x, start_y), (goal_x, goal_y))

    # Instantiate a_star_solver
    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1])
    path = a_star_solver.a_star_fwd()

    if path:  # If a path was found
        extracted_path = extract_path(path)  # Convert the start position to a tuple
        start_pos = (start[0], start[1]) # Convert the goal position to a tuple
        goal_pos = (goal[0], goal[1])  # Convert the goal position to a tuple
        print("Generating path visualization...")
        visualize_path(maze, extracted_path, start_pos, goal_pos) # Visualize the path
    else:
        print("No path found.")
        

def run_a_star_backward(maze_file):
    print(f"Running A* backward on {maze_file}...")
    maze = read_maze_from_file(maze_file)  # Read the maze
    start, goal = choose_random_positions(maze)  # Choose start and goal positions

   
    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1])
    path = a_star_solver.a_star_bkw()

    if path:
        extracted_path = extract_path(path)  
        start_pos = (start[0], start[1])  
        goal_pos = (goal[0], goal[1])  
        print("Generating path visualization...")
        visualize_path(maze, extracted_path, start_pos, goal_pos)
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
        maze_file_path = None  

        if option in ["3", "4"]:
            maze_file = get_maze_file()  
            maze_file_path = f"HW1/mazes/{maze_file}"  

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
