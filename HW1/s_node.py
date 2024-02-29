import random
""" 
    class for successor node organizing info relevant to search state values influencing A* search decisions with respect to which state to explore as 
    the next step wrt finding the shorest path to th egoal, and minmizng the number of sub-optimal/incorrect paths are explored.
    When finished it can retrun the relevant path to the algorithm as a linked list.
    This can be used to reconstruct the shortest path and the value of the state at each step
    
    There can exist multiple nodes representing the same state simultaneously. The node is merely a representation of the state
    and preserves the decsion/state hsitory producing that specific path to the state. It's possible (likely) that multiple paths
    to the same state. A properly constructed A* algorithm will prioritize exploration of next states based on optimal values of the variables
    tracked by this node. The node is not the state, it is just an abstraction of the state for use by the the linked list
    representing a specific path from the start state to the goals state
"""
class sNode:
    def __init__(self, x = None, y = None, prev = None,break_tie=True):
        """
        """
        self.x,self.y=x,y
        self.g = float('inf')
        self.h =0
        self.prev = prev
        self.break_tie_small = break_tie
     
    def update_prev(self, prev_node):
        self.prev = prev_node
    def get_prev(self):
        return self.prev
    
    def get_coord(self):
        return (self.x, self.y)
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    
    """
    Methods for updating values relevant to A* decision making
    - h score: respresent value of distance 
      estimate from current state to the the goal, by a heuristic provided by the A* algorithm
      in this case manhattan distance. A better heuristic can vastly reduce the number of
      suboptimal paths explored before finding the shortest path to the goal (or fidning that the goal)
      is unreachable

      g score: tracks the cost of reaching the current state from the start state
      in this case the cost is uniform equal to the cost of reaching the previous state
      plus an action cost of 1. This results in a marginal action cost of 1, but different problem
      context can exist and be represented with dynamic and/or variable action cost, and naive counting of
      steps will be insufficient for these porblem domains.

      f score: combined score of the cost to the state and the estimated cost from the state to the goal
      used for priotorizing which node to choose next, with the smallest value being prioritized for exploration
      in the context of finding the shorest path 
    """
    def set_h(self,h_value):
        self.h = h_value
    def get_h(self):
        return self.h
    
    def update_g(self, g_value):
        self.g = g_value
    def get_g(self):
        return self.g
    def init_g(self):
        if self.prev:
            self.update_g(self.prev.get_G())

    def get_f(self):
        return self.g + self.h 
    
    """
    Defines rank of node based on state values for use by priority queue representing
    exploratory frontier of succesors nodes to explore 
    """

    def __lt__(self,other):
        if (self.g + self.h) == (other.g + other.h):
            #if self.g == other.g:
            #    return (random.random() <0.5)
            if self.break_tie_small:
                return (self.g) < (other.g)
            return (self.g) > (other.g)    
        return (self.g + self.h) < (other.g + other.h)
    
    def __iter__(self):
        for each in self.__dict__.values():
            yield each
    