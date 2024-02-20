import queue
""" 
    class for successor node organizing info relevant to A* search decisions

"""

class sNode:
    def __init__(self, x = None, y = None,  prev = None):
        """
        """
        self.x = x
        self.y = y
        self.prev = prev

    def get_prev(self):
        return self.prev

    def get_coord(self):
        return(self.x, self.y)

class PriorityQueueWrapper:
    def __init__(self,priority,obj):
        self.priority = priority
        self.obj = obj
    def __lt__(self,other):
        return self.priority < other.priority