import random
from generate_mazes import generate_and_save_mazes
from maze_driver import display_all_mazes
from maze_driver import display_maze
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

def display_one_maze(file_path):
    print(f"Displaying {file_path}...")
    display_maze(file_path)

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


def run_a_star_forward(maze_file, break_tie_small=True):

    print(f"Running A* Forward on {maze_file} with {'smaller' if break_tie_small else 'larger'} g-value preference...")
    maze = read_maze_from_file(maze_file)  # This returns the maze as a list of lists (True/False values)
    start, goal = choose_random_positions(maze)  #  return ((start_x, start_y), (goal_x, goal_y))

    # Instantiate a_star_solver
    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=break_tie_small)
    path = a_star_solver.a_star_fwd()

    extracted_path = extract_path(path)  # Convert the start position to a tuple
    start_pos = (start[0], start[1]) # Convert the goal position to a tuple
    goal_pos = (goal[0], goal[1])  # Convert the goal position to a tuple
    visited_nodes = set(a_star_solver.visited.keys())  # Convert the visited nodes to a set
    print("Generating path visualization...")
    visualize_path(maze, extracted_path, start_pos, goal_pos, visited_nodes, maze_file, F"A* Forward {'smaller' if break_tie_small else 'larger'} g-value preference")
    

def run_a_star_backward(maze_file):
    print(f"Running A* backward on {maze_file}...")
    maze = read_maze_from_file(maze_file)  # Read the maze
    start, goal = choose_random_positions(maze)  # Choose start and goal positions

   
    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=False) #always larger gvalue thus break_tie_small=False
    path = a_star_solver.a_star_bkw()

    if path:
        extracted_path = extract_path(path)  
        start_pos = (start[0], start[1])  
        goal_pos = (goal[0], goal[1])  
        visited_nodes = set(a_star_solver.visited.keys())
        print("Generating path visualization...")
        visualize_path(maze, extracted_path, start_pos, goal_pos, visited_nodes, maze_file, "A* Backward larger g-value preference")
    else:
        print("No path found.")


def main():

    while True:
        print("\nPlease select an option:")
        print("1 - Generate 50 mazes")
        print("2 - View a maze")
        print("3 - View all 50 mazes")
        print("4 - Run A* Forward (smallest g-value)")
        print("5 - Run A* Forward (largest g-value)")
        print("6 - Run A* Backward (largest g-value)")
        print("7 - Run A* Adaptive")
        print("8 - Maze with start/goal points (no search)")
        print("9 - Exit")

        option = input("Enter your choice: ")
        maze_file_path = None  

        if option in ["2", "4", "5", "6", "7"]:
            random.seed(42)
            maze_file = get_maze_file()  
            maze_file_path = f"HW1/mazes/{maze_file}"  

        if option == "1":
            generate_mazes()
        elif option == "2" and maze_file_path:
            display_one_maze(maze_file_path)
        elif option == "3":
            view_mazes()
        
        elif option == "4" and maze_file_path: #smallest gvalue
            run_a_star_forward(maze_file_path, break_tie_small=True)
        elif option == "5" and maze_file_path: #largest gvalue
            run_a_star_forward(maze_file_path, break_tie_small=False)
        elif option == "6" and maze_file_path:
            run_a_star_backward(maze_file_path)
        elif option == "7" and maze_file_path:
            run_a_star_adaptive(maze_file_path)
        elif option == "8":
            maze = read_maze_from_file(maze_file_path)
            start, goal = choose_random_positions(maze)
            print("Generating path visualization...")
            visualize_path(maze, [start, goal], start, goal, set(), maze_file_path, "Maze with points no search")
        elif option == "9":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose a valid option (1-6).")


if __name__ == "__main__":

    main()
