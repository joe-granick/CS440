import heapq as q
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
        self.start=(start_x,start_y)
        self.goal=(goal_x,goal_y)
        self.expanded = 0
        self.adaptive = False
        self.break_tie_small = break_tie_small
        self.min_goal_dist = float('inf')
        self.search_count = defaultdict(lambda: float('inf'))
        self.count=0
        self.shortest_path_length  = float('inf')
        self.blocked = set()
        self.search_paths=[]

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
    def check_neighbors(self, node):
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.is_valid((x+node.get_x(),y+node.get_y())):
             if not self.path[y+node.get_y()][x+node.get_x()]:
                 self.blocked.add((x+node.get_x(),y+node.get_y()))

    def is_valid(self, coord):
        x, y = coord[0], coord[1]
        r, c = len(self.path), len(self.path[0])
        return 0 <= x < c and 0 <= y < r and (x,y) not in self.blocked
    
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
    
    def a_star_search(self):
        """Conducts the actual A* search
            Finds shortest path based on current knowledge of        
        """
        current_node = q.heappop(self.frontier)
        self.check_neighbors(current_node)
        path_blocked = False
        X,Y=0,1
        while current_node.get_g()<self.visited[self.goal]:
            new_g = current_node.get_g()+1
            successors = self.generate_succ(current_node)
            self.expanded += 1
            for succ in successors:
                if succ.get_coord() in self.search_count and self.search_count[succ.get_coord()]<self.count:
                    self.visited[succ.get_coord()] = float('inf')
                    self.search_count[succ.get_coord()] = self.count
            
                if succ.get_coord() not in self.visited or new_g < self.visited[succ.get_coord()]:
                    succ.update_g(new_g)
                    succ.set_h(self.manhattan_dist(succ.get_x(), succ.get_y(), self.goal[X], self.goal[Y]))
                    q.heappush(self.frontier, succ)
                    self.visited[succ.get_coord()]=new_g
            current_node = q.heappop(self.frontier)
            if not self.path[current_node.get_y()][current_node.get_x()]:
                return current_node.get_prev()
        #self.search_paths.append(current_node)
        return current_node
 
    
    def a_star_repeated(self, update=[]):
        """
        Runs A* search to maintain optimal path in environments where path ~costs can change between actions
        """
        self.count = 0
        self.search_count = defaultdict()
        self.frontier=[]
        self.visited[self.goal]=float('inf')
        X,Y=0,1
        start=s_node.sNode(self.start[X], self.start[Y])
        start.update_g(0)  # Start node g-value is 0
        start.set_h(self.manhattan_dist(self.start[X],self.start[Y],self.goal[X],self.goal[Y]))
        self.visited[self.start]=start.get_g()
        self.search_count[self.start]=self.count
        while (start.get_coord())!=(self.goal):
            self.count+=1
            q.heappush(self.frontier,start)
            self.blocked.add(start.get_coord())
            start = self.a_star_search()
            current_path = start
            while current_path:
                print(current_path.get_coord())
                current_path = current_path.get_prev()
            print()

    
    # def a_star_adaptive(self,update=[]):
    #     """
    #     Repeats A* search to maintain shortest path like repeated, but after initial shortest path is found
    #     it provides a better heuristic for all previosuly visited nodes based on the previos search. This should reduce 
    #     number and length of the new optimal path especially in cases where the new shortest path is similiar to the previous  
    #     """
    #     adaptive_searches = []
    #     self.frontier = []  # Reset the frontier for the next search
    #       # Reset visited nodes for the next search
        
    #     shortest_path = self.a_star_fwd()  # Forward A* search
    #     print("Shortest Path:", shortest_path.get_coord())
        
    #     rev_shortest_path = self.a_star_bkw()  # Backward A* search
    #     if rev_shortest_path:
    #         print(rev_shortest_path.get_coord())
    #         self.start_x, self.start_y = rev_shortest_path.get_prev().get_coord()
            
    #         print("Reversed Shortest Path:", rev_shortest_path.get_coord())
    #     self.adaptive = True
    #     # Update starting position for the next iteration

    #     while (self.start_x, self.start_y) != (self.goal_x, self.goal_y):
    #         self.count+=1
    #         shortest_path = self.a_star_fwd()
    #         if not shortest_path:
    #             break
    #         shortest_path_length = shortest_path.get_g()
            
            

    #         rev_shortest_path = self.a_star_bkw()
    #         if not rev_shortest_path:
    #             break
    #         rev_shortest_path_length = rev_shortest_path.get_g()
            
            
    #         if rev_shortest_path_length == shortest_path_length:
    #             rev_shortest_path = rev_shortest_path.get_prev()
    #             self.start_x, self.start_y = rev_shortest_path.get_coord()
    #             # Update heuristic for adaptive behavior
    #             self.update_heuristics(shortest_path, rev_shortest_path)
                
    #             # Simulate changes in the environment
    #             if update: 
    #                 block_x, block_y = update.pop(random.randint(0, len(update)-1))
    #                 self.path[block_y][block_x] = False
    #                 for row in range(len(self.path)):
    #                     for col in range(len(self.path[row])):
    #                         if self.path[row][col]:
    #                             print('O', end='')
    #                         else:
    #                             print('X', end='')
    #                     print()
    #                 print()
    #                 self.visited = defaultdict()
    #         adaptive_searches.append(shortest_path)
    #         print("Shortest Path Found:", shortest_path.get_coord())

    #         # Check for termination conditions
    #         if shortest_path.get_g() >= self.shortest_path_length:
    #             print("No new path found. Exiting adaptive search.")
    #             break
            
    #         else:
    #             self.shortest_path_length = shortest_path.get_g()

    #     return adaptive_searches
    
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
        
        repeated_test_maze = aStar(path=test_path, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
        repeated_test_maze.a_star_repeated()
        #node = repeated_test_maze.a_star_repeated()
        # while node:
        #     print(node.get_coord())
        #     node = node.get_prev()
                
if __name__ == "__main__":
    aStar().main()
