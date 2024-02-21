class PriorityQueue:
    def __init__(self):
        # Initialize an empty list to store elements with priorities
        self.elements = []

    def empty(self):
        # Check if the priority queue is empty
        return len(self.elements) == 0
    
    def qsize(self):
        return len(self.elements)

    def put(self, item, priority):
        # Add a new element with its priority to the priority queue
        self.elements.append((priority, item))
        # Restore heap property by performing heapify up
        self._heapify_up(len(self.elements) - 1)

    def get(self):
        if not self.empty():
            # Swap the first and last elements, pop the last (min priority) element, and heapify down
            self._swap(0, len(self.elements) - 1)
            item = self.elements.pop()[1]
            self._heapify_down(0)
            return item
        else:
            raise IndexError("PriorityQueue is empty")

    def _swap(self, i, j):
        # Swap elements at indices i and j in the heap
        temp = self.elements[i]
        self.elements[i] = self.elements[j]
        self.elements[j] = temp

    def _heapify_up(self, index):   # Move the element up the tree until the heap property is restored
        while index > 0:
            # Calculate the parent index
            parent_index = (index - 1) // 2
            # If the current element has a higher priority than its parent, swap them
            if self.elements[index] < self.elements[parent_index]:
                self._swap(index, parent_index)
                index = parent_index
            else:
                # If no swap is needed, break out of the loop
                break

    def _heapify_down(self, index): # Move the element down the tree until the heap property is restored
        while True:
            # Calculate the indices of the left and right children
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            # Find the smallest of the current element and its left and right children
            if left_child_index < len(self.elements) and self.elements[left_child_index] < self.elements[smallest]:
                smallest = left_child_index

            if right_child_index < len(self.elements) and self.elements[right_child_index] < self.elements[smallest]:
                smallest = right_child_index

            # If the smallest element is not the current element, swap them
            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                # If no swap is needed, break out of the loop
                break
