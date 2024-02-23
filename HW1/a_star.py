#from Queue import PriorityQueue, PrioritizedItem
import queue as q
import heapq
from queue import PriorityQueue
from collections import defaultdict 
import grid_world
import random
import s_node
from s_node import PriorityQueueWrapper




class aStar:
    """ 
    class to implement A* search variations for fidning the shortest path through a maze 
    on a grid
    """
    def __init__(self, file_path, start_x=None, start_y=None, goal_x=None, goal_y=None):
        self.path = self.read_maze_from_file(file_path)
        self.frontier = q.PriorityQueue()
        self.visited = defaultdict()
        self.start_x, self.start_y = start_x, start_y
        self.goal_x, self.goal_y = goal_x, goal_y
        self.expanded = 0
    
    def read_maze_from_file(self, file_path):
        maze = []
        with open(file_path, 'r') as file:
            for line in file:
                maze.append([char == 'O' for char in line.strip()])
        return maze

    def manhattan_dist(self, s_x, s_y, goal_x, goal_y):
        """estimates heuristic by distance without any blocked paths"""
        return abs(goal_x - s_x) + abs(goal_y - s_y)
    
    def generate_succ(self, node):
        x,y = node.get_coord()[0],node.get_coord()[1]
        return [(x - 1, y), (x + 1, y), 
                (x, y - 1), (x, y + 1)]

    def isValid(self, x, y):
        r, c = len(self.path), len(self.path[0])
        if x < 0 or y < 0: return False
        if x >= c or y >= r: return False
        return self.path[y][x]

    
    def reconstruct_path(self, end_node):
        """Reconstructs the path from start to goal by backtracking from the goal node."""
        path = []
        current = end_node
        while current is not None:
            path.append(current.get_coord())
            current = current.get_prev()
        path.reverse()  # The path is constructed backwards, so we need to reverse it
        return path

    
        
    def a_star_fwd(self):
        start_node = s_node.sNode(x=self.start_x, y=self.start_y)
        # Initially putting the start node into the queue with priority 0
        self.frontier.put(PriorityQueueWrapper(0, start_node))
        self.visited[(start_node.x, start_node.y)] = True  # Mark start as visited
        
        while not self.frontier.empty():
            current_wrapper = self.frontier.get()
            current_node = current_wrapper.obj  #access the node via .obj
            if (current_node.x, current_node.y) == (self.goal_x, self.goal_y):
                return self.reconstruct_path(current_node)
                
            for x, y in self.generate_succ(current_node):  # Use current_node here
                if self.isValid(x, y) and not self.visited.get((x, y)):
                    self.visited[(x, y)] = True
                    h_cost = self.manhattan_dist(x, y, self.goal_x, self.goal_y)
                    succ = s_node.sNode(x, y, current_node)
                    #wrap the successor node and its heuristic cost in PriorityQueueWrapper
                    self.frontier.put(PriorityQueueWrapper(h_cost, succ))
                    
        return None  # Return None if no path is found


    def a_star_bwd(self):
        current_node = s_node.sNode(x=self.goal_x, y=self.goal_y)
        self.frontier.put(PriorityQueueWrapper(0, current_node))
        self.visited[(current_node.x, current_node.y)] = True  # Mark goal as visited
        
        while not self.frontier.empty():
            current_wrapper = self.frontier.get()
            current_node = current_wrapper.obj  # Correctly access the node via .obj
            if (current_node.x, current_node.y) == (self.start_x, self.start_y):
                return self.reconstruct_path(current_node)


                
            for x, y in self.generate_succ(current_node):
                if self.isValid(x, y) and not self.visited.get((x, y)):
                    self.visited[(x, y)] = True
                    h_cost = self.manhattan_dist(x, y, self.start_x, self.start_y)
                    succ = s_node.sNode(x, y, current_node)
                    self.frontier.put(PriorityQueueWrapper(h_cost, succ))  # Insert successor with heuristic cost
        
        return None  # No path found

            
    def main(self):
        # Example method to run A* and print results (you can adjust this as needed)
        node = self.a_star_bwd()  # Assuming this is the method you want to use
        if node:
            print("Path found:")
            while node:
                print(node.get_coord(), ":", self.visited[node])
                node = node.get_prev()
        else:
            print("No path found.")

        
if __name__ == "__main__":
    aStar().main()