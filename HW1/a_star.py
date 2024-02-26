import heapq as q
from collections import defaultdict
import s_node

class aStar:
    """ 
    Class to implement A* search variations for finding the shortest path through a maze 
    on a grid
    """
    def __init__(self, path=None, start_x=None, start_y=None, goal_x=None, goal_y=None, break_tie_small=True):
        self.path = path
        self.frontier = []
        self.visited = defaultdict()
        self.start_x, self.start_y = start_x, start_y
        self.goal_x, self.goal_y = goal_x, goal_y
        self.expanded = 0
        self.adaptive = False
        self.break_tie_small = break_tie_small
        self.min_goal_dist = float('inf')

    def manhattan_dist(self, s_x, s_y, goal_x, goal_y):
        """ Estimates heuristic by distance without any blocked paths """
        return abs(goal_x - s_x) + abs(goal_y - s_y)
    
    def generate_succ(self, node):
        successors = []
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
             succ = s_node.sNode(node.get_x() + x, node.get_y() + y, node, break_tie=self.break_tie_small)
             if self.is_valid(succ.get_coord()):
                 successors.append(succ)
        return successors

    def is_valid(self, coord):
        x, y = coord[0], coord[1]
        r, c = len(self.path), len(self.path[0])
        return 0 <= x < c and 0 <= y < r and self.path[y][x]
    
    def a_star(self, current, g_x, g_y, g_val, prev=None):
        """
        Calculates necessary info to track state for A* search
        """
        current.update_g(g_val)
        if not self.adaptive or current.get_coord() not in self.visited: 
            current.set_h(self.manhattan_dist(current.get_x(), current.get_y(), g_x, g_y))
        else:
            current.set_h(self.visited[(g_x, g_y)] - self.visited[current.get_coord()])
        current.update_prev(prev)
        return current
    

    def a_star_fwd(self):
        """
        Performs A* search from start to goal, aiming for the shortest path.
        """
        start_node = s_node.sNode(self.start_x, self.start_y, None, self.break_tie_small)
        start_node.update_g(0)  # Start node g-value is 0
        start_node.set_h(self.manhattan_dist(self.start_x, self.start_y, self.goal_x, self.goal_y))  # Set initial heuristic

        self.frontier = []
        q.heappush(self.frontier, start_node)
        self.visited = {}  # Reset or initialize visited dict
        self.visited[(self.start_x, self.start_y)] = start_node.get_f()

        goal_node = None

        while self.frontier:
            current_node = q.heappop(self.frontier)
            
            # If goal is found, break from the loop
            if (current_node.get_x(), current_node.get_y()) == (self.goal_x, self.goal_y):
                goal_node = current_node
                break

            successors = self.generate_succ(current_node)
            for succ in successors:
                new_g = current_node.get_g() + 1  # Assuming each step cost is 1
                new_f = new_g + succ.get_h()  # f = g + h

                if (succ.get_x(), succ.get_y()) not in self.visited or new_f < self.visited[(succ.get_x(), succ.get_y())]:
                    succ.update_g(new_g)
                    succ.set_h(self.manhattan_dist(succ.get_x(), succ.get_y(), self.goal_x, self.goal_y))
                    self.visited[(succ.get_x(), succ.get_y())] = new_f
                    q.heappush(self.frontier, succ)

        if goal_node:
            print("Goal found")
            return goal_node
        else:
            print("No path to the goal")
            return None

    
    def a_star_bkw(self):
        """
        Performs A* search from goal to start, aiming for the shortest path.
        """
        # Initialize the goal node as the start for backward search
        start_node = s_node.sNode(self.goal_x, self.goal_y, None, self.break_tie_small)
        start_node.update_g(0)  # Goal node g-value is 0 for backward search
        start_node.set_h(self.manhattan_dist(self.goal_x, self.goal_y, self.start_x, self.start_y))  # Set initial heuristic towards the original start

        self.frontier = []
        q.heappush(self.frontier, start_node)
        self.visited = {} 
        self.visited[(self.goal_x, self.goal_y)] = start_node.get_f()

        original_start_node = None

        while self.frontier:
            current_node = q.heappop(self.frontier)

            # If original start is found, break from the loop
            if (current_node.get_x(), current_node.get_y()) == (self.start_x, self.start_y):
                original_start_node = current_node
                break

            successors = self.generate_succ(current_node)
            for succ in successors:
                new_g = current_node.get_g() + 1  # each step cost is 1
                new_f = new_g + succ.get_h()  # f = g + h

                if (succ.get_x(), succ.get_y()) not in self.visited or new_f < self.visited[(succ.get_x(), succ.get_y())]:
                    succ.update_g(new_g)
                    # Heuristic now points towards the original start
                    succ.set_h(self.manhattan_dist(succ.get_x(), succ.get_y(), self.start_x, self.start_y))
                    self.visited[(succ.get_x(), succ.get_y())] = new_f
                    q.heappush(self.frontier, succ)

        if original_start_node:
            print("Original start found via backward search")
            return original_start_node
        else:
            print("No path to the original start")
            return None
    
    def a_star_adaptive(self):
        """
        Runs A* search adaptively, updating heuristics based on previous searches.
        """
        adaptive_searches = []
        self.adaptive = True  # Enable adaptive mode for heuristic updates

        # Perform the initial A* search
        initial_goal_node = self.a_star_fwd()
        if not initial_goal_node:
            print("No path found in the initial search.")
            return adaptive_searches

        adaptive_searches.append(initial_goal_node)
        last_path_length = initial_goal_node.get_g()  # Store the length/cost of the initial path

        # Update heuristic values based on the first search
        self.update_heuristics(initial_goal_node)

        while True:
            a_star = self.a_star_fwd()
            if a_star and a_star.get_g() != last_path_length:
                adaptive_searches.append(a_star)
                self.update_heuristics(a_star)
                last_path_length = a_star.get_g()  # Update for the next iteration's comparison
            else:
                break  # Exit if no new path is found or if the path length hasn't changed

        return adaptive_searches

    
    def update_heuristics(self, goal_node):
        """
        Updates the heuristic values (h) of nodes based on the most recent search.
        """
        current = goal_node
        goal_g_value = goal_node.get_g()  # The total cost from start to goal found in the most recent search

        while current:
            self.visited[current.get_coord()] = goal_g_value - current.get_g()
            current = current.get_prev()
    
    def reverse_path(self, node):
        """
        Reverses path of a node
        """
        search_path = []
        rev_search = []
        while node.get_prev():
            search_path.append(node.get_prev())
            node = node.get_prev()
        while len(search_path) > 0:
            rev_search.append(search_path.pop())
        return rev_search
        
    def get_expanded(self):
        """
        Returns the number of expanded nodes
        """
        expanded_nodes = self.expanded
        return expanded_nodes
            
    def main(self):
        start_x, start_y = 2, 4
        goal_x, goal_y = 4, 4

        test_path = [
            [True, True, True, True, True],
            [True, True, False, True, True],
            [True, True, False, False, True],
            [True, True, False, False, True],
            [True, True, True, False, True]
        ]
        
        fwd_test_maze = aStar(path=test_path, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
        node = fwd_test_maze.a_star_fwd()
        if node:
            while node.get_prev():
                print(node.get_prev().get_coord(), ": ", fwd_test_maze.visited[node.get_prev().get_coord()])
                node = node.get_prev()
        print("Expanded nodes: ", fwd_test_maze.get_expanded())
        
        bkw_test_maze = aStar(path=test_path, start_x=goal_x, start_y=goal_y, goal_x=start_x, goal_y=start_y)
        node = bkw_test_maze.a_star_bkw()
        if node:
            while node.get_prev():
                print(node.get_prev().get_coord(), ": ", bkw_test_maze.visited[node.get_prev().get_coord()])
                node = node.get_prev()
        print("Expanded nodes: ", bkw_test_maze.get_expanded())

        adaptive_test_maze = aStar(path=test_path, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
        adaptive = adaptive_test_maze.a_star_adaptive()
        for path in adaptive:
            while path.get_prev():
                print(path.get_prev().get_coord(), ": ", adaptive_test_maze.visited[path.get_prev().get_coord()], end='')
                path = path.get_prev()
        print()
        print("Expanded nodes: ", adaptive_test_maze.get_expanded())
        
if __name__ == "__main__":
    aStar().main()