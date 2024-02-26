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
        Repeats A* from start to goal until the shortest path to goal is reached
        """
        start = self.a_star(s_node.sNode(self.start_x, self.start_y), self.goal_x, self.goal_y, 0)
        self.visited[(self.start_x, self.start_y)] = 0
        if not self.adaptive: 
            self.visited[(self.goal_x, self.goal_y)] = float('inf')
        q.heappush(self.frontier, start)
        goal = None

        while self.frontier:
            current = q.heappop(self.frontier)
            self.expanded += 1
            if current.get_coord() == (self.goal_x, self.goal_y):
                goal = current
                break
            successors = self.generate_succ(current)
            new_cost = self.visited[current.get_coord()] + 1
            for succ in successors:
                if succ.get_coord() not in self.visited or new_cost < self.visited[succ.get_coord()]:
                    q.heappush(self.frontier, succ)
                    succ.update_g(new_cost)
                    self.visited[succ.get_coord()] = new_cost
            
        if goal:
            print("Goal found")
            return goal
        
        print("No path to the goal")
        return None
    
    def a_star_bkw(self):
        """
        Repeats A* from goal to start until the shortest path to goal is reached
        """
        goal = self.a_star(s_node.sNode(self.goal_x, self.goal_y), self.start_x, self.start_y, 0)
        self.visited[(self.goal_x, self.goal_y)] = 0
        if not self.adaptive: 
            self.visited[(self.start_x, self.start_y)] = float('inf')
        q.heappush(self.frontier, goal)
        start = None

        while self.frontier:
            current = q.heappop(self.frontier)
            self.expanded += 1
            if current.get_coord() == (self.start_x, self.start_y):
                start = current
                break
            successors = self.generate_succ(current)
            new_cost = self.visited[current.get_coord()] + 1
            for succ in successors:
                if succ.get_coord() not in self.visited or new_cost < self.visited[succ.get_coord()]:
                    q.heappush(self.frontier, succ)
                    succ.update_g(new_cost)
                    self.visited[succ.get_coord()] = new_cost
            
        if start:
            print("Start found")
            return start
        
        print("No path to the start")
        return None
    
    def a_star_adaptive(self):
        """
        Runs A* search adaptively
        """
        adaptive_searches = []
        a_star = self.a_star_fwd()
        self.adaptive = True
        while a_star:
            adaptive_searches.append(a_star)
            a_star = self.reverse_path(a_star)
            a_star = self.a_star_fwd()
        return adaptive_searches
    
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
