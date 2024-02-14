import random

"""class to initiliaze grid with start stae goal state and obstacles"""
class GridWorld:
    def __init__(self, rows, cols):
        """
        
        initialize RxC size grid as the search space
        
        path creates a matrix with all cells initiialized to True representing
        an open path 
            
        """

        self.rows = rows
        self.cols = cols


        self.path = [
               [False for x in range(self.cols)]
                for y in range(self.rows)
               ]

    
    def block_path(self,x, y):
        """helper function, blocks a cell by setting its coordinates to False"""
        self.path[y][x] = False

    def valid_move(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows and (x, y) not in visited 

    def generate_moves(self, x, y):
        return[
                (x-1, y), (x+1, y),
                (x, y-1), (x, y+1)
                ]

    def dfs(self, x, y):
        """depth first search implementation for creating the maze"""
        
        if not valid_move(x,y): return

        visited.add(x, y)


        # leaves cell unvisited 30% prob
        if random.random() < 0.3: 
            return

        self.path[y][x] = True
        moves = generate_moves(x, y)
        random.shuffle(moves)

        for x, y in moves:
            dfs(x, y)

    def create_maze(self):
        """
        Generates maze on grid by starting at a random point and perfroming a DFS
        for all cells and randomly blocks cells with a 30% probability
        """

        start_x = random.randint(0,self.cols-1)
        start_y = random.randint(0,self.rows-1)
        visited = set()
        
        dfs(start_x, start_y)

    def print_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print self.path[row][col]
            print

    def main(self):

        grid = GridWorld(101,101)
        grid.create_maze

