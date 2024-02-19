from queue import PriorityQueue
from collection import defaultdict 
import GridWorld
import random

""" 

class to implement A* search variations for fidning the shortest path through a maze 
on a grid

"""


class aStar:
    def __init__(self, grid):
        """
        """
        self.grid = GridWorld()
        self.frontier = PriorityQueue()
        self.visited = defaultdict()
        self.start
        self.goal
        

    def initialize_search(self):
        self.goal = rand_coord()
        start = rand_coord()
        while start == self.goal:
            start = rand_coord()
        self.start = start
        

    def rand_coord(self):
        rx = random.randint(length(self.grid))
        ry = random.randint(length(self.grid))    
        while not self.grid.valid_move(rx,ry):
            rx = random.randint(length(self.grid))
            ry = random.randint(length(self.grid))    
        return = (rx,ry)
        
    def a_star_fwd(s_x, s_y):
        return

    def a_star_bck:
        return

    def a_star_rpt:
        return

    def manhattan_dist(s_x, s_y, goal_x, goal_y):
        """estimates heuristic by distance without any blocked paths"""
        return abs((goal_x - s_x) + (goal_y - s_y))

    def succ_cost():


    
    def main(self):
        maze = GridWorld(101, 101)
        maze.create_maze()
        maze.print_grid()
        print()

        a_star_fwd = aStar(maze)

        
if __name__ == "__main__":
    aStar().main()