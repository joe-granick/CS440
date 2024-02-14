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
                [True for y in range(self.cols)]
                for x in range(self.rows)
                ]

    
    def block_path(self,x, y):
        """helper function, blocks a cell by setting its coordinates to False"""
        self.path[x][y] = False


