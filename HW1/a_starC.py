#from Queue import PriorityQueue, PrioritizedItem
from pq import PriorityQueue as q
from collections import defaultdict 
import grid_world
import random
import s_node



class aStar:
    """ 
    class to implement A* search variations for fidning the shortest path through a maze 
    on a grid
    """
    def __init__(self, path= None, start_x = None, start_y = None, goal_x = None, goal_y = None):
        self.path = path
        self.frontier = q.PriorityQueue()
        self.visited = defaultdict()
        self.start_x, self.start_y = start_x, start_y
        self.goal_x, self.goal_y = goal_x, goal_y
        self.expanded = 0

    def manhattan_dist(self, s_x, s_y, goal_x, goal_y):
        """estimates heuristic by distance without any blocked paths"""
        return (abs((goal_x - s_x) + (goal_y - s_y)))
    
    def generate_succ(self, node):
        x,y = node.get_coord()[0],node.get_coord()[1]
        return [(x - 1, y), (x + 1, y), 
                (x, y - 1), (x, y + 1)]

    def isValid(self, coord):
        r,c = len(self.path),len(self.path[0])
        if coord[0] < 0 or coord[1] < 0:return False
        if coord[0] >= c or coord[1] >= r: return False
        return True
    def adaptive_h(self, node):
        if node.get_coord    
        
    def a_star_fwd(self):
        """
            calculates shortest path from goal to path using standard forward A* with
            manhattan distance heuristic
        """
        #initialize starting cell
        current = s_node.sNode(x=self.start_x, y=self.start_y)
        self.visited[(self.start_x,self.start_y)] = 0
        self.frontier.put(s_node.PriorityQueueWrapper(float('inf'), current))

        while not self.frontier.empty():
            current = self.frontier.get().obj
            if current.get_coord() == (self.goal_x, self.goal_y):
                print("path found")
                return current
            successors = self.generate_succ(current)
            for succ_coord in successors:
                x = succ_coord[0]
                y = succ_coord[1]
                print(x,",", y)
                succ = s_node.sNode(x, y, current)
                
                if not self.isValid(succ_coord):
                    self.visited[(x,y)] = float('inf')
                    #print("out of bounds")
                elif not self.path[y][x]:
                    self.visited[(x,y)] = float('inf')
                    #print(x,",",y,": ", print(x,",",y,": ",self.path[y][x]), " ", float('inf'))
                else:
                    self.visited[(x,y)] = self.visited[(x,y)]+1
                    h_cost = self.manhattan_dist(x, y,self.goal_x, self.goal_y)
                    cost_est = h_cost + self.visited[(x,y)]
                    print(x,",",y,": ",self.path[y][x], "placed at prio: ", cost_est)
                    self.frontier.put(s_node.PriorityQueueWrapper(cost_est, succ))
        print("no path found")
        return None

            
    def main(self):
        """
        maze = grid_world.GridWorld(10, 10)
        maze.create_maze()
        maze.print_grid()
        print()
        """
        start_x,start_y = 0,0
        goal_x,goal_y = 5,5
        test_path = [
                    [True, False, True, True, True, True, True, False, False, True],
                    [True, False, True, True, True, True, True, False, False, True],
                    [True, False, True, True, True, True, True, True, False, True],
                    [True, True, False, True, True, True, True, True, False, True],
                    [False,True,False,False, False, False, True, False, False, True],
                    [True, True, False, False, True, True, True, False, False, True],
                    [True, True, False, False, False, True, True, True, False, True],
                    [True, True, False, True, True, True, True, False, False, True],
                    [True, True, True, True, True, True, True, True, False, True],
                    [True, True, True, True, True, True, True, True, True, True]
                    ]
        
        fwd_test_maze = aStar(path=test_path,
                            start_x=start_x,start_y=start_y,
                            goal_x=goal_x, goal_y=goal_y)
        node = fwd_test_maze.a_star_fwd()
        while node.get_prev():
            print(node.get_prev().get_coord(), ": ", test_maze.visited[node.get_prev()])
            node = node.get_prev()
        
        
        bkw_test_maze = aStar(path=test_path,
                                start_x=goal_x,start_y=goal_y,
                                goal_x=start_x,goal_y=start_y)
        node = fwd_test_maze.a_star_fwd()
        while node.get_prev():
            print(node.get_prev().get_coord(), ": ", test_maze.visited[node.get_prev()])
            node = node.get_prev()
        
if __name__ == "__main__":
    aStar().main()