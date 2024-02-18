import random

class GridWorld:
    def __init__(self, rows, cols):
        """
        Initializes a grid with specified rows and columns.

        The grid is represented by the 'path' matrix with all cells initially set to False,
        indicating a blocked path.

        The 'visited' set is used to keep track of visited cells during maze generation.
        """
        self.rows = rows
        self.cols = cols
        self.path = [[False for x in range(self.cols)] for y in range(self.rows)]
        self.visited = set()

    def block_path(self, x, y):
        """
        Blocks a cell in the grid by setting its coordinates to False.

        :param x: x-coordinate of the cell.
        :param y: y-coordinate of the cell.
        """
        self.path[y][x] = False

    def valid_move(self, x, y):
        """
        Checks if a move to the specified coordinates (x, y) is valid.

        :param x: x-coordinate of the cell.
        :param y: y-coordinate of the cell.
        :return: True if the move is valid, False otherwise.
        """
        return 0 <= x < self.cols and 0 <= y < self.rows and (x, y) not in self.visited

    def generate_moves(self, x, y):
        """
        Generates possible moves from a given cell.

        :param x: x-coordinate of the cell.
        :param y: y-coordinate of the cell.
        :return: List of possible moves.
        """
        return [(x - 1, y), (x + 1, y), 
                (x, y - 1), (x, y + 1)]

    def dfs(self, x, y):
        """
        Depth-first search implementation for creating the maze.

        :param x: x-coordinate of the cell.
        :param y: y-coordinate of the cell.
        """
        stack = [(x,y)]
        
        while stack:
            x,y = stack.pop()
            #print(x,y)
            #print()

            if not self.valid_move(x,y):
                continue
            
            self.visited.add((x, y))
            if random.random() < 0.3:
                continue
            self.path[y][x] = True

            #if random.random() < 0.3:
            #    continue

            #print(x, y)
            moves = self.generate_moves(x, y)
            random.shuffle(moves)    
            for nx, ny in moves:
                #print("(",nx,",",ny,") ")
                if self.valid_move(nx,ny):
                    stack.append((nx,ny))
        #print()


    def create_maze(self):
        """
        Generates a maze on the grid by starting at a random point and recursively calls DFS
        for all cells, randomly blocking cells with a 30% probability.
        """
        start_x = random.randint(0, self.cols - 1)
        start_y = random.randint(0, self.rows - 1)
        self.visited = set()
        self.dfs(start_x, start_y)

    def print_grid(self):
        """
        Prints the grid, displaying 'O' for open path and 'X' for blocked path.
        """
        
    
        for row in range(self.rows):
            for col in range(self.cols):
                if self.path[row][col]:
                    print('O', end='')
                else:
                    print('X', end='')
            print()

    def main(self):
        """
        Main function to create an instance of GridWorld, generate a maze, and print the grid.
        """
        #grid = GridWorld(5, 5)
        #grid.create_maze()
        #grid.print_grid()

        grid = GridWorld(101, 101)
        grid.create_maze()
        grid.print_grid()

if __name__ == "__main__":
    GridWorld(101,101).main()
