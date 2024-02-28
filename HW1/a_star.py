from pq import PriorityQueue as q
from collections import defaultdict
import s_node
import random

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
        self.search_count = defaultdict()
        self.count=0
        self.shortest_path_length  = float('inf')

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
        goal_node = None
        # Initialize the goal in visited if not adaptive or correct logic accordingly
        if not self.adaptive:
            self.visited[goal.get_coord()] = goal.get_g()

        while self.frontier:
            current_node = q.heappop(self.frontier)
            if current_node.get_coord() == goal.get_coord():
                goal_node = current_node
                break
            print(self.expanded, " nodes expanded: ", current_node.get_coord(), " g: ", current_node.get_g(), " f: ", current_node.get_f()," start:", self.start_x, self.start_y, " goal: ", self.goal_x, self.goal_y)
            self.expanded += 1
            successors = self.generate_succ(current_node)
            for succ in successors:
                new_g = current_node.get_g() + 1  # Assuming each step cost is 1
                if succ.get_coord() not in self.visited or new_g < self.visited[succ.get_coord()]:
                    succ.update_g(new_g)
                    succ.set_h(self.manhattan_dist(succ.get_x(), succ.get_y(), goal.get_x(), goal.get_y()))
                    q.heappush(self.frontier, succ)
                    self.visited[succ.get_coord()] = new_g

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
        if not self.adaptive: self.visited = defaultdict()
        self.frontier=[]
        start_node = s_node.sNode(self.start_x, self.start_y, None, self.break_tie_small)
        start_node.update_g(0)  # Start node g-value is 0
        start_node.set_h(self.manhattan_dist(self.start_x, self.start_y, self.goal_x, self.goal_y))
        
        goal_node = s_node.sNode(self.goal_x, self.goal_y, None, self.break_tie_small)
        #goal_node.update_g(float('inf'))  # Start node g-value is 0
        #goal_node.set_h(self.manhattan_dist(self.goal_x, self.goal_y, self.goal_x, self.goal_y))
        
        q.heappush(self.frontier, start_node)
        self.visited[start_node.get_coord()] = start_node.get_g()
        goal = self.a_star_search(goal=goal_node)
        return goal 

    
    def a_star_bkw(self):
        """
        Performs A* search from goal to start, aiming for the shortest path.
        """
        if not self.adaptive: self.visited = defaultdict()
        self.frontier=[]
        # Initialize the goal node as the start for backward search
        start_node = s_node.sNode(self.goal_x, self.goal_y, None, self.break_tie_small)
        start_node.update_g(0)  # Goal node g-value is 0 for backward search
        start_node.set_h(self.manhattan_dist(self.goal_x, self.goal_y, self.start_x, self.start_y))  # Set initial heuristic towards the original start
        
        goal_node = s_node.sNode(self.start_x, self.start_y, None, self.break_tie_small)
        #goal_node.update_g(float('inf'))  # Goal node g-value is 0 for backward search
        #goal_node.set_h(self.manhattan_dist(self.start_x, self.start_y,self.start_x, self.start_y,))  # Set initial heuristic towards the original start
        
        q.heappush(self.frontier, start_node)
        self.visited[start_node.get_coord()] = start_node.get_g()
        
        goal = self.a_star_search(goal=goal_node)
        return goal
    
    def a_star_repeated(self, update=[]):
        """
        Runs A* search to maintain optimal path in environments where path costs can change between actions
        """
        
        #self.count = 0
        #self.search_count = defaultdict()
        
        shortest_path = self.a_star_fwd()
        shortest_paths = []
        
        print(shortest_path.get_coord())
        rev_shortest_path = self.a_star_bkw()
        print(rev_shortest_path.get_coord())
        self.start_x, self.start_y = rev_shortest_path.get_prev().get_coord()
        
        while (self.start_x, self.start_y)!=(self.goal_x,self.goal_y):
            self.visited = defaultdict()
            shortest_path = self.a_star_fwd()
            if not shortest_path:
                break
            shortest_path_length = shortest_path.get_g()
            rev_shortest_path = self.a_star_bkw()
            if not rev_shortest_path:
                break
        
            rev_shortest_path_length = rev_shortest_path.get_g()
            
            if rev_shortest_path_length == shortest_path_length:
                rev_shortest_path = rev_shortest_path.get_prev()
                self.start_x, self.start_y = rev_shortest_path.get_coord()
                if update:
                    self.visited = defaultdict() 
                    block_x, block_y=update.pop(random.randint(0,len(update)-1))
                    self.path[block_y][block_x]=False
                    for row in range(len(self.path)):
                        for col in range(len(self.path[row])):
                            if self.path[row][col]:
                                print('O', end='')
                            else:
                                print('X', end='')
                        print()
                    print()
            shortest_paths.append(shortest_paths)
        return shortest_path


    def a_star_adaptive(self,update=[]):
        """
        Repeats A* search to maintain shortest path like repeated, but after initial shortest path is found
        it provides a better heuristic for all previosuly visited nodes based on the previos search. This should reduce 
        number and length of the new optimal path especially in cases where the new shortest path is similiar to the previous  
        """
        adaptive_searches = []
        self.frontier = []  # Reset the frontier for the next search
          # Reset visited nodes for the next search
        
        shortest_path = self.a_star_fwd()  # Forward A* search
        print("Shortest Path:", shortest_path.get_coord())
        
        rev_shortest_path = self.a_star_bkw()  # Backward A* search
        print("Reversed Shortest Path:", rev_shortest_path.get_coord())
        self.adaptive = True
        # Update starting position for the next iteration
        self.start_x, self.start_y = rev_shortest_path.get_prev().get_coord()
        while (self.start_x, self.start_y) != (self.goal_x, self.goal_y):
            shortest_path = self.a_star_fwd()
            if not shortest_path:
                break
            shortest_path_length = shortest_path.get_g()
            
            

            rev_shortest_path = self.a_star_bkw()
            if not rev_shortest_path:
                break
            rev_shortest_path_length = rev_shortest_path.get_g()
            
            
            if rev_shortest_path_length == shortest_path_length:
                rev_shortest_path = rev_shortest_path.get_prev()
                self.start_x, self.start_y = rev_shortest_path.get_coord()
                # Update heuristic for adaptive behavior
                self.update_heuristics(shortest_path, rev_shortest_path)
                
                # Simulate changes in the environment
                if update: 
                    block_x, block_y = update.pop(random.randint(0, len(update)-1))
                    self.path[block_y][block_x] = False
                    for row in range(len(self.path)):
                        for col in range(len(self.path[row])):
                            if self.path[row][col]:
                                print('O', end='')
                            else:
                                print('X', end='')
                        print()
                    print()
                    self.visited = defaultdict()
            adaptive_searches.append(shortest_path)
            print("Shortest Path Found:", shortest_path.get_coord())

            # Check for termination conditions
            if shortest_path.get_g() >= self.shortest_path_length:
                print("No new path found. Exiting adaptive search.")
                break
            
            else:
                self.shortest_path_length = shortest_path.get_g()

        return adaptive_searches
    
    def update_heuristics(self, forward_path, backward_path):
        """
        Updates the heuristic values (h) for previously visited nodes based on the previous search.
        """
        current = backward_path
        while current:
            coord = current.get_coord()
            self.visited[coord] = forward_path.get_g() - current.get_g()
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

    

        repeated_test=[[True for x in range(len(test_path))] for y in range(len(test_path[0]))]
        blocked_cells=[]
     
        repeated_test[4][3]=False
        repeated_test[3][2]=False
        
        blocked_cells.append((2,2))
        blocked_cells.append((2,1))
        blocked_cells.append((3,1))
        blocked_cells.append((3,3))
        
        repeated_test_maze = aStar(path=repeated_test, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
        repeated_test_maze.a_star_repeated(blocked_cells)
        
        adaptive_test_maze = aStar(path=repeated_test, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
        adaptive_maze=adaptive_test_maze.a_star_adaptive(blocked_cells)
        for path in adaptive_maze:
            while path.get_prev():
                print(path.get_prev().get_coord(), ": ", path.get_prev().get_g(), end='')
                path = path.get_prev()
        print()
        print("Expanded nodes: ", adaptive_test_maze.get_expanded())        
if __name__ == "__main__":
    aStar().main()
