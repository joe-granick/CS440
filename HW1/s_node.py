import queue
""" 
    class for successor node organizing info relevant to A* search decisions

"""

class sNode:
    def __init__(self, x = None, y = None, prev = None,break_tie=False):
        """
        """
        self.x,self.y=x,y
        self.g,self.h = float('inf'),None
        self.prev = prev
        self.break_tie = break_tie
    
    def update_prev(self, prev_node):
        self.prev = prev_node
    def get_prev(self):
        return self.prev
    
    def get_coord(self):
        return(self.x, self.y)
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    
    def set_h(self,h_value):
        self.h = h_value
    def get_h(self):
        return self.h
    
    def update_g(self, g_value):
        self.g = g_value
    def get_g(self):
        return self.g

    def get_f(self):
        return self.g + self.h 

    def __lt__(self,other):
        if (self.g + self.h) == (other.g + other.h):
            if self.break_tie:
                return (self.g) < (other.g)    
        return (self.g + self.h) < (other.g + other.h)
    
    def __iter__(self):
        for each in self.__dict__.values():
            yield each
    