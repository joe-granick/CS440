#from Queue import PriorityQueue, PrioritizedItem
import heapq as q
from collections import defaultdict 
import s_node

class aStar:
    """ 
    class to implement A* search variations for fidning the shortest path through a maze 
    on a grid
    """
    def __init__(self, path= None, start_x = None, start_y = None, goal_x = None, goal_y = None, break_tie_small=True):
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
        """estimates heuristic by distance without any blocked paths"""
        return abs(goal_x - s_x) + abs(goal_y - s_y)
    
    def generate_succ(self, node):
        succesors = []
        for x,y in [(-1,0),(1,0),(0,-1),(0,1)]:
             succ = s_node.sNode(node.get_x()+x,node.get_y()+y,node,break_tie=self.break_tie_small)
             if self.isValid(succ.get_coord()):
                 succesors.append(succ)
        return succesors

    def isValid(self, coord):
        x,y = coord[0],coord[1]
        r,c = len(self.path),len(self.path[0])
        return 0<=x<c and 0<=y<c and self.path[y][x]
    
    def a_star(self, current, g_x, g_y, g_val, prev=None):
        """
        calculates necessary info to track state for A* search
        """
        current.update_g(g_val)
        if not self.adaptive or current.get_coord() not in self.visited: 
            current.set_h(self.manhattan_dist(current.get_x(), current.get_y(), g_x, g_y))
        else:
            current.set_h(self.visited[(g_x,g_y)]-self.visited[current.get_coord()])
        current.update_prev(prev)
        return current
    
    def reverse_path(self,node):
        """
        Reverses path of a node
        Needed to set up adaptive a_star
        """
        search_path = []
        rev_search = []
        while node.get_prev():
            search_path.append(node.get_prev())
            node = node.get_prev()
        while len(search_path)>0:
            rev_search.append(search_path.pop())
        return rev_search
        

    def a_star_fwd(self):
        """
            repeats A* from start to goal until shortest path to goal is reached
        """
        #initialize starting cell
        start = self.a_star(s_node.sNode(self.start_x, self.start_y), self.goal_x, self.goal_y, 0)
        #goal = self.a_star(s_node.sNode(self.goal_x, self.goal_y), self.goal_x, self.goal_y, float('inf'))
        self.visited[(self.start_x,self.start_y)] = 0
        if not self.adaptive: self.visited[(self.goal_x,self.goal_y)] = float('inf')
        q.heappush(self.frontier,start)
        goal = None

        while self.frontier[0].get_f() < self.visited[(self.goal_x,self.goal_y)]: 
            current = q.heappop(self.frontier)
            self.expanded+=1
            succesors = self.generate_succ(current)
            new_cost = self.visited[current.get_coord()]+1
            for succ in succesors:
                succ = self.a_star(succ, self.goal_x, self.goal_y,new_cost, current)
                if succ.get_coord() == (self.goal_x, self.goal_y) and new_cost < self.visited[(self.goal_x, self.goal_y)]:
                    goal = succ 
                if succ.get_coord() not in self.visited or new_cost < self.visited[succ.get_coord()]:
                    q.heappush(self.frontier,succ)
                    succ.update_g(new_cost)
                    self.visited[succ.get_coord()] = new_cost
            
        if goal:
            print("goal found")
            return goal
        
        print("no path to goal")
        return None
    
    def a_star_bkw(self):
        """
            repeats A* from goal to start until shortest path to goal is reached
        """
        #initialize starting cell
        start = self.a_star(s_node.sNode(self.start_x, self.start_y), self.start_x, self.start_y, float('inf'))
        goal = self.a_star(s_node.sNode(self.goal_x, self.goal_y), self.start_x, self.start_y, 0)
        self.visited[(self.start_x,self.start_y)] = float('inf')
        self.visited[(self.goal_x,self.goal_y)] = 0
        q.heappush(self.frontier,goal)
        
        while self.frontier: 
            current = q.heappop(self.frontier)
            self.expanded+=1
            if current.get_coord() == start.get_coord():
                start.update_g(current.get_g()+1)
                start.update_prev(current)
                self.visited[start.get_coord()]=start.get_g()
                print("start found")
                return start
            succesors = self.generate_succ(current)
            new_cost = self.visited[current.get_coord()]+1
            for succ in succesors:
                succ = self.a_star(succ, self.start_x, self.start_y,new_cost, current)
                if succ.get_coord() not in self.visited or new_cost < self.visited[succ.get_coord()]:
                    q.heappush(self.frontier,succ)
                    succ.update_g(new_cost)
                    self.visited[succ.get_coord()] = new_cost
        print("no path found")
        return None

    def a_star_adaptive(self):
        """
        runs fwd A* search
        then continuously runs with g_values provided as updated h_value
        in order to be adaptive to changing environment
        returns a list containing each path
        """
        adaptive_searches = []
        a_star = self.a_star_fwd()
        self.adaptive = True
        while a_star:
            adaptive_searches.append(a_star)
            a_star = self.reverse_path(a_star)
            a_star = self.a_star_fwd()
        return adaptive_searches
    
    def get_expanded(self):
        expanded_nodes = self.expanded
        return expanded_nodes
            
    def main(self):
        """
        maze = grid_world.GridWorld(10, 10)
        maze.create_maze()
        maze.print_grid()
        print()
        """
        start_x,start_y = 2,4
        goal_x,goal_y = 4,4
 
        test_path = [
                    [True, True, True, True, True],
                    [True, True, False, True, True],
                    [True, True, False, False, True],
                    [True, True, False, False, True],
                    [True, True, True, False, True]
                    ]
        
        
        fwd_test_maze = aStar(path=test_path,
                            start_x=start_x,start_y=start_y,
                            goal_x=goal_x, goal_y=goal_y)
        node = fwd_test_maze.a_star_fwd()
        while node.get_prev():
            print(node.get_prev().get_coord(), ": ", fwd_test_maze.visited[node.get_prev().get_coord()])
            node = node.get_prev()
        print("expanded nodes ",fwd_test_maze.get_expanded())
        
        bkw_test_maze = aStar(path=test_path,
                                start_x=goal_x,start_y=goal_y,
                                goal_x=start_x,goal_y=start_y)
        node = bkw_test_maze.a_star_bkw()
        while node.get_prev():
            print(node.get_prev().get_coord(), ": ", bkw_test_maze.visited[node.get_prev().get_coord()])
            node = node.get_prev()
        print("expanded nodes ",bkw_test_maze.get_expanded())

        adaptive_test_maze = aStar(path=test_path,
                            start_x=start_x,start_y=start_y,
                            goal_x=goal_x, goal_y=goal_y)
        adaptive = adaptive_test_maze.a_star_adaptive()
        for i in range(0,len(adaptive)-1):
            path = adaptive[i]
            while path.get_prev():
                print(path.get_prev().get_coord(), ": ", adaptive_test_maze.visited[path.get_prev().get_coord()], end='')
                path = path.get_prev()
        print()
        print("expanded nodes ",adaptive_test_maze.get_expanded())
        
if __name__ == "__main__":
    aStar().main()