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
    
    def a_star_search(self, goal):
        if not self.adaptive:
            self.visited[goal.get_coord()] = goal.get_g()
            goal_node = None
        while self.frontier and self.frontier[0].get_g()<self.visited[goal.get_coord()]:
            current_node = q.heappop(self.frontier)
            
            # If goal is found, break from the loop
            if current_node.get_coord() == goal.get_coord():
                goal_node = current_node
                break
            
            print(self. expanded, " nodes expanded: ", current_node.get_coord()," g: ", current_node.get_g(), " f: ", current_node.get_f())
            successors = self.generate_succ(current_node)
            self.expanded+=1
            for succ in successors:
                new_g = current_node.get_g() + 1  # Assuming each step cost is 1
                if succ.get_coord() not in self.visited or new_g < self.visited[(succ.get_x(), succ.get_y())]:
                    succ.update_g(new_g)
                    succ.set_h(self.manhattan_dist(succ.get_x(), succ.get_y(), goal.get_x(), goal.get_y()))
                    self.visited[succ.get_coord()] = new_g
                    q.heappush(self.frontier, succ)

        if goal_node:
            print("Goal found")
            return goal_node
        else:
            print("No path to the goal")
            return None

    def a_star_fwd(self):
        """
        Performs A* search from start to goal, aiming for the shortest path.
        """
        self.frontier=[]
        start_node = s_node.sNode(self.start_x, self.start_y, None, self.break_tie_small)
        start_node.update_g(0)  # Start node g-value is 0
        start_node.set_h(self.manhattan_dist(self.start_x, self.start_y, self.goal_x, self.goal_y))
        
        goal_node = s_node.sNode(self.goal_x, self.goal_y, None, self.break_tie_small)
        goal_node.update_g(float('inf'))  # Start node g-value is 0
        goal_node.set_h(self.manhattan_dist(self.goal_x, self.goal_y, self.goal_x, self.goal_y))
        
        q.heappush(self.frontier, start_node)
        self.visited[start_node.get_coord()] = start_node.get_g()
        goal = self.a_star_search(goal=goal_node)
        return goal 

    
    def a_star_bkw(self):
        """
        Performs A* search from goal to start, aiming for the shortest path.
        """
        self.frontier=[]
        # Initialize the goal node as the start for backward search
        start_node = s_node.sNode(self.goal_x, self.goal_y, None, self.break_tie_small)
        start_node.update_g(0)  # Goal node g-value is 0 for backward search
        start_node.set_h(self.manhattan_dist(self.goal_x, self.goal_y, self.start_x, self.start_y))  # Set initial heuristic towards the original start
        
        goal_node = s_node.sNode(self.start_x, self.start_y, None, self.break_tie_small)
        goal_node.update_g(float('inf'))  # Goal node g-value is 0 for backward search
        goal_node.set_h(self.manhattan_dist(self.start_x, self.start_y,self.start_x, self.start_y,))  # Set initial heuristic towards the original start
        
        q.heappush(self.frontier, start_node)
        self.visited[start_node.get_coord()] = start_node.get_g()
        
        goal = self.a_star_search(goal=goal_node)
        return goal
    
    def a_star_adaptive(self):
        """
        Runs A* search adaptively, updating heuristics based on previous searches.
        """
        adaptive_searches = []
          # Enable adaptive mode for heuristic updates

        # Perform the initial A* search
        initial_goal_node = self.a_star_fwd()
        if not initial_goal_node:
            print("No path found in the initial search.")
            return adaptive_searches

        adaptive_searches.append(initial_goal_node)
        last_path_length = initial_goal_node.get_g()  # Store the length/cost of the initial path
        self.adaptive = True
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
        return self.expanded
            
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
        
        bkw_test_maze = aStar(path=test_path, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
        node = bkw_test_maze.a_star_bkw()
        if node:
            while node.get_prev():
                print(node.get_prev().get_coord(), ": ", bkw_test_maze.visited[node.get_prev().get_coord()])
                node = node.get_prev()
        print("Expanded nodes: back", bkw_test_maze.get_expanded())

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
