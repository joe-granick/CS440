import random
from generate_mazes import generate_and_save_mazes
from maze_driver import display_all_mazes
from maze_driver import display_maze
from a_star import aStar
from path_visualizer import visualize_path, visualize_path_adaptive


def extract_path(goal_node):
    path = []
    current = goal_node
    while current is not None:
        path.append((current.x, current.y))  
        current = current.prev
    return path


def extract_paths(goal_nodes): #for adaptive search
    paths = []
    for goal_node in goal_nodes:
        path = []
        current = goal_node
        while current is not None:
            path.append((current.x, current.y))
            current = current.prev
        path.reverse()
        paths.append(path)
    return paths


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

def list_of_blocked_cells(maze):
    list_of = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == False:
                list_of.append((i,j))
    return list_of


def choose_random_positions(maze):
    random.seed(42)
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
    maze = read_maze_from_file(maze_file)
    start, goal = choose_random_positions(maze) # the seed should work on this
    print(f"Selected Start: {start}, Goal: {goal}")  # Debug 

    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=break_tie_small)
    list_of_blocked = list_of_blocked_cells(maze)
    path = a_star_solver.a_star_fwd()
    visited_nodes = set(a_star_solver.visited.keys())
    extracted_path = extract_path(path)
    expanded_nodes = a_star_solver.expanded

    print("Generating path visualization...")
    visualize_path(maze, extracted_path, start, goal, visited_nodes, expanded_nodes, maze_file, f"A* Forward {'smaller' if break_tie_small else 'larger'} g-value preference")

def run_a_star_repeat(maze_file, break_tie_small=True):
    print(f"Running A* Repeated on {maze_file} with {'smaller' if break_tie_small else 'larger'} g-value preference...")
    maze = read_maze_from_file(maze_file)
    start, goal = choose_random_positions(maze) # the seed should work on this
    print(f"Selected Start: {start}, Goal: {goal}")  # Debug 

    for r in maze:
        for c in maze[r]:
            maze[r][c] = True
    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=break_tie_small)
    list_of_blocked = list_of_blocked_cells(maze)
    path = a_star_solver.a_star_repeated(list_of_blocked)
    visited_nodes = set(a_star_solver.visited.keys())
    extracted_path = extract_path(path)
    expanded_nodes = a_star_solver.expanded

    print("Generating path visualization...")
    visualize_path(maze, extracted_path, start, goal, visited_nodes, expanded_nodes, maze_file, f"A* Repeated {'smaller' if break_tie_small else 'larger'} g-value preference")



def run_a_star_backward(maze_file):
    print(f"Running A* backward on {maze_file}...")
    maze = read_maze_from_file(maze_file)  # Read the maze
    start, goal = choose_random_positions(maze)  # the seed should work on this
    print(f"Selected Start: {start}, Goal: {goal}")  # Debug print

   
    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=False) #always larger gvalue thus break_tie_small=False
    path = a_star_solver.a_star_bkw()

    if path:
        extracted_path = extract_path(path)  
        start_pos = (start[0], start[1])  
        goal_pos = (goal[0], goal[1])  
        visited_nodes = set(a_star_solver.visited.keys())
        expanded_nodes = a_star_solver.expanded
        print("Generating path visualization...")
        visualize_path(maze, extracted_path, start, goal, visited_nodes, expanded_nodes, maze_file, "A* Backward larger g-value preference")
    else:
        print("No path found.")



def run_a_star_adaptive(maze_file):
    print(f"Running A* adaptive on {maze_file}...")
    maze = read_maze_from_file(maze_file)
    start, goal = choose_random_positions(maze)
    print(f"Selected Start: {start}, Goal: {goal}")  # Debug print

    a_star_solver = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=False)
    adaptive_searches = a_star_solver.a_star_adaptive()

    if adaptive_searches:
        extracted_paths = extract_paths(adaptive_searches)  
        for i, path in enumerate(extracted_paths):
            start_pos = (start[0], start[1])
            goal_pos = (goal[0], goal[1])
            visited_nodes = set(a_star_solver.visited.keys())
            expanded_nodes = a_star_solver.expanded
            print(f"Visualizing adaptive search {i+1}...")
            visualize_path_adaptive(maze, path, start_pos, goal_pos, visited_nodes, expanded_nodes, maze_file, f"A* Adaptive Search {i+1}", i+1)
    else:
        print("No path found.")



def compare_a_star_g_values():
    output_lines = ["Expanded cell count:\n", "Maze #   | A* Forward (Large G) | A* Forward (Small G)\n"]

    total_expanded_large = 0
    total_expanded_small = 0

    for maze_num in range(50):
        maze_file = f"HW1/mazes/maze{maze_num}.txt"
        maze = read_maze_from_file(maze_file)

        start, goal = choose_random_positions(maze)  # the seed should work on this

        # Initialize the A* solver with break_tie_small=False for large g-value preference
        a_star_large_g = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=False)
        path_large_g = a_star_large_g.a_star_fwd()
        expanded_large = a_star_large_g.expanded
        total_expanded_large += expanded_large

        # Initialize the A* solver with break_tie_small=True for small g-value preference
        a_star_small_g = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=True)
        path_small_g = a_star_small_g.a_star_fwd()
        expanded_small = a_star_small_g.expanded
        total_expanded_small += expanded_small

        output_lines.append(f"Maze {maze_num:2} : {expanded_large:15}       | {expanded_small:15}\n")

    avg_expanded_large = total_expanded_large / 50
    avg_expanded_small = total_expanded_small / 50

    output_lines.append(f"\nTotal expanded nodes: {total_expanded_large:15} | {total_expanded_small:15}\n")
    output_lines.append(f"Average expanded nodes: {avg_expanded_large:15} | {avg_expanded_small:15}\n")




    # Write the comparison results to a file
    with open("a_star_comparison_results.txt", "w") as file:
        file.writelines(output_lines)
    print("Comparison completed and results saved to a_star_comparison_results.txt.")



def compare_a_star_forward_backward():
    output_lines = ["Expanded cell count:\n", "Maze #   | A* Forward (Large G) | A* Backward (Large G)\n"]

    total_expanded_fwd = 0
    total_expanded_bkw = 0

    for maze_num in range(50):
        maze_file = f"HW1/mazes/maze{maze_num}.txt"
        maze = read_maze_from_file(maze_file)

        start, goal = choose_random_positions(maze)  # Ensure consistent start and goal for both runs

        # A* Forward with large g-value preference
        a_star_fwd_large_g = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=False)
        a_star_fwd_large_g.a_star_fwd()
        expanded_fwd_large = len(a_star_fwd_large_g.visited)
        total_expanded_fwd += expanded_fwd_large

        # A* Backward (large g-value preference)
        a_star_bkw = aStar(path=maze, start_x=goal[0], start_y=goal[1], goal_x=start[0], goal_y=start[1], break_tie_small=False) # Note: Start and goal are swapped
        a_star_bkw.a_star_bkw()
        expanded_bkw = len(a_star_bkw.visited)
        total_expanded_bkw += expanded_bkw

        output_lines.append(f"Maze {maze_num:2} : {expanded_fwd_large:15}       | {expanded_bkw:15}\n")

    avg_expanded_fwd = total_expanded_fwd / 50
    avg_expanded_bkw = total_expanded_bkw / 50

    output_lines.append(f"\nTotal expanded nodes: {total_expanded_fwd:15} | {total_expanded_bkw:15}\n")
    output_lines.append(f"Average expanded nodes: {avg_expanded_fwd:15} | {avg_expanded_bkw:15}\n")

    # Write the comparison results to a file
    with open("a_star_fwd_bkw_comparison_results.txt", "w") as file:
        file.writelines(output_lines)
    print("Comparison of A* Forward (Large G) and A* Backward completed and results saved to a_star_fwd_bkw_comparison_results.txt.")



def compare_a_star_forward_adaptive():
    output_lines = ["Expanded cell count:\n", "Maze #   | A* Forward (Large G) | A* Adaptive (Large G)\n"]

    total_expanded_fwd = 0
    total_expanded_adaptive = 0

    for maze_num in range(50):
        maze_file = f"HW1/mazes/maze{maze_num}.txt"
        maze = read_maze_from_file(maze_file)
        
        start, goal = choose_random_positions(maze)  # Ensure consistent start and goal for both runs

        # A* Forward with large g-value preference
        a_star_fwd_large_g = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=False)
        a_star_fwd_large_g.a_star_fwd()
        expanded_fwd_large = len(a_star_fwd_large_g.visited)
        total_expanded_fwd += expanded_fwd_large

        # Adaptive A*
        a_star_adaptive = aStar(path=maze, start_x=start[0], start_y=start[1], goal_x=goal[0], goal_y=goal[1], break_tie_small=False)
        adaptive_searches = a_star_adaptive.a_star_adaptive()
        
        # Assuming adaptive_searches returns a list of goal nodes, and the total visited count is desired
        # Directly use the visited count of the last adaptive search for comparison
        # This assumes the aStar object retains its state and visited count after the last adaptive search
        if adaptive_searches:  # Check if any adaptive searches were successful
            expanded_adaptive = len(a_star_adaptive.visited)  # Use the visited count from the last search
            total_expanded_adaptive += expanded_adaptive

        output_lines.append(f"Maze {maze_num:2} : {expanded_fwd_large:15}       | {expanded_adaptive:15}\n")

    avg_expanded_fwd = total_expanded_fwd / 50
    avg_expanded_adaptive = total_expanded_adaptive / 50

    output_lines.append(f"\nTotal expanded nodes: {total_expanded_fwd:15} | {total_expanded_adaptive:15}\n")
    output_lines.append(f"Average expanded nodes: {avg_expanded_fwd:15} | {avg_expanded_adaptive:15}\n")

    # Write the comparison results to a file
    with open("a_star_fwd_adaptive_comparison_results.txt", "w") as file:
        file.writelines(output_lines)
    print("Comparison of A* Forward (Large G) and A* Adaptive completed and results saved to a_star_fwd_adaptive_comparison_results.txt.")



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
        print("9 - Compare A* Forward by g-value")
        print("10 - Compare A* Forward/Backward by large g-value")
        print("11 - Run repeated A*")
        print("12 - Compare A* Forward/Adaptive by large g-value")
        print("13 - Exit")

        option = input("Enter your choice: ")
        maze_file_path = None  

        if option in ["2", "4", "5", "6", "7", "8", "11"]:
            random.seed(42)
            maze_file = get_maze_file()  
            maze_file_path = f"HW1/mazes/{maze_file}"  

        if option == "1":
            generate_mazes()

        elif option == "2" and maze_file_path:
            display_one_maze(maze_file_path)

        elif option == "3":
            view_mazes()
        
        elif option == "4" and maze_file_path: #small gvalue
            run_a_star_forward(maze_file_path, break_tie_small=True)

        elif option == "5" and maze_file_path: #large gvalue
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
            compare_a_star_g_values()

        elif option == "10":
            compare_a_star_forward_backward()

        elif option == "11":
            run_a_star_repeat(maze_file)
        
        elif option == "12":
            compare_a_star_forward_adaptive()

        elif option == "13":
            print("Exiting program.")
            break

        else:
            print("Invalid option. Please choose a valid option (1-6).")



if __name__ == "__main__":
    main()
