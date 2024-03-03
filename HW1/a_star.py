import heapq as q
from collections import defaultdict
import s_node
import random
import pygame

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class aStar:
    """ 
    Class to implement A* search variations for finding the shortest path through a maze 
    on a grid
    """
    def __init__(self, path=None, start_x=None, start_y=None, goal_x=None, goal_y=None, break_tie_small=True):
        self.path = path
        self.frontier = []
        self.visited = defaultdict(lambda: float('inf'))
        self.start=(start_x,start_y)
        self.goal=(goal_x,goal_y)
        self.expanded = 0
        self.adaptive = False
        self.break_tie_small = break_tie_small
        self.min_goal_dist = float('inf')
        self.search_count = defaultdict(lambda: 0)
        self.count=0
        self.shortest_path_length  = float('inf')
        self.blocked = set()
        self.search_paths=[]
        self.search_trajectory=[]
        self.blocked_cells=[]
        self.blocked_list=[]

        # Initialize Pygame screen size
        self.screen_width = len(path[0]) * 30
        self.screen_height = len(path) * 30
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("A* Pathfinding")

        # Initialize clock for controlling frame rate
        self.clock = pygame.time.Clock()

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

    def a_star_search(self,start):
        """Conducts the actual A* search
            Finds shortest path based on current knowledge of        
        """
        X,Y=0,1
        q.heappush(self.frontier,start)
        while self.frontier[0].get_f()<self.visited[self.goal]:
            current_node = q.heappop(self.frontier)
            new_g = current_node.get_g()+1
            successors = self.generate_succ(current_node)
            self.expanded += 1
            for succ in successors:
                if  succ.get_coord() not in self.search_count or self.search_count[succ.get_coord()]<self.count:
                    self.visited[succ.get_coord()] = float('inf')
                    self.search_count[succ.get_coord()] = self.count
            
                if new_g < self.visited[succ.get_coord()]:
                    succ.update_g(new_g)
                    succ.set_h(self.manhattan_dist(succ.get_x(), succ.get_y(), self.goal[X], self.goal[Y]))
                    q.heappush(self.frontier, succ)
                    self.visited[succ.get_coord()]=new_g
        return self.frontier[0]

    def a_star_repeated(self, update=[]):
        """
        Runs A* search to maintain optimal path in environments where path ~costs can change between actions
        """
        X,Y=0,1
        start=s_node.sNode(self.start[X], self.start[Y])
        
        while (start.get_coord())!=(self.goal):
            start.update_g(0)  # Start node g-value is 0
            start.set_h(self.manhattan_dist(self.start[X],self.start[Y],self.goal[X],self.goal[Y]))
            self.search_count[self.start]=self.count
            self.visited[start.get_coord()]=start.get_g()
            self.visited[self.goal]=float('inf')
            self.count+=1
            goal = self.a_star_search(start)
            current_path = self.reverse_path(goal)
            
            for node in current_path:
                print(node.get_coord())
            print()
            
            self.search_trajectory.append(current_path) 
            start = self.traverse_path(current_path)
            
            print(start.get_coord())
            print()
            start.update_prev(None)
            self.frontier=[]
            

    def traverse_path(self,path):
        for node in path:
            if not self.path[node.get_y()][node.get_x()]:
                self.blocked.add(node.get_coord())
                self.blocked_list.append(node.get_coord())
                print(node.get_coord(), " blocked")
                
                self.search_paths.append(self.reverse_path(node.get_prev()))
                
                return node.get_prev()
        self.search_paths.append(self.reverse_path(node))
        return node

    def get_trajectory(self):return self.search_trajectory
    def get_search(self):return self.search_paths
    
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
        while node:
            search_path.append(node)
            node = node.get_prev()
        while search_path:
            rev_search.append(search_path.pop())
        return rev_search
    def get_blocked(self):
        return self.blocked_list
        
    def get_expanded(self):
        """
        Returns the number of expanded nodes
        """
        return self.expanded
            
    def draw_grid(self):
        """
        Draw the grid representation of the maze on the Pygame screen
        """
        WHITE = (255, 255, 255)
        BLACK = (0,0,0)

        for y in range(len(self.path)):
            for x in range(len(self.path[0])):
                rect = pygame.Rect(x * 30, y * 30, 30, 30)
                #if (x,y) in block:
                #    pygame.draw.rect(self.screen, BLACK, rect)
                
                pygame.draw.rect(self.screen, WHITE, rect)

    def draw_path(self, path, color):
        """
        Draw the path on the Pygame screen
        """
        for node in path:
            print(node.get_coord())
            rect = pygame.Rect(node.get_x() * 30, node.get_y() * 30, 30, 30)
            pygame.draw.rect(self.screen, color, rect)
        print()
    
    def draw_blocked(self, path, color,index):
        """
        Draw the path on the Pygame screen
        """
        for node in range(index):
            print(node)
            rect = pygame.Rect(path[node][0]*30,path[node][1]*30, 30, 30)
            pygame.draw.rect(self.screen, color, rect)
        print()

    def a_star_step(self):
        """
        Perform one step of the A* algorithm
        """
        if not self.frontier:
            return False  # Algorithm finished
        current_node = q.heappop(self.frontier)
        if current_node.get_coord() == self.goal:
            return True  # Goal reached

        new_g = current_node.get_g() + 1
        successors = self.generate_succ(current_node)
        self.expanded += 1
        for succ in successors:
            if succ.get_coord() not in self.search_count or self.search_count[succ.get_coord()] < self.count:
                self.visited[succ.get_coord()] = float('inf')
                self.search_count[succ.get_coord()] = self.count

            if new_g < self.visited[succ.get_coord()]:
                succ.update_g(new_g)
                succ.set_h(self.manhattan_dist(succ.get_x(), succ.get_y(), self.goal[0], self.goal[1]))
                q.heappush(self.frontier, succ)
                self.visited[succ.get_coord()] = new_g

        return None

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

        # Create an instance of the aStar class and pass the maze path
        astar = aStar(path=test_path, start_x=start_x, start_y=start_y, goal_x=goal_x, goal_y=goal_y)
        astar.a_star_repeated()
    

        running = True
        paused = False
        finished = False

        # Get the search paths and trajectory
        search_trajectory = astar.get_trajectory()
        search_path = astar.get_search()
        blocked_path = astar.get_blocked()

        # Index variables to iterate over the paths and trajectory
        path_index = 0
        trajectory_index = 0
        # Draw the grid
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("space")
                        paused = not paused  # Toggle pause
                    elif event.key == pygame.K_r:
                        paused = False
                        finished = False

            if not paused and not finished:
                astar.draw_grid()
                if trajectory_index < len(search_trajectory):
                    # Draw the current path
                    astar.draw_path(search_trajectory[trajectory_index], GREEN)
                    astar.draw_path(search_path[trajectory_index], RED)
                    astar.draw_blocked(blocked_path, BLACK,trajectory_index)
                    trajectory_index+=1
                else:
                    
                    finished = True

            # Clear the screen
            #self.screen.fill(BLACK)

           

            # Draw visited nodes
            # for coord, g_val in astar.visited.items():
            #     if g_val != float('inf'):
            #         rect = pygame.Rect(coord[0] * 30, coord[1] * 30, 30, 30)
            #         pygame.draw.rect(self.screen, BLUE, rect)

            pygame.display.flip()

            # Control frame rate
            self.clock.tick(1)  # Adjust as needed

        pygame.quit()

if __name__ == "__main__":
    test_path = [
            [True, True, True, True, True],
            [True, True, False, True, True],
            [True, True, False, False, True],
            [True, True, False, False, True],
            [True, True, True, False, True]
        ]
    aStar(path = test_path).main()
        