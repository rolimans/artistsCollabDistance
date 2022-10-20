import heapq

# Wrapper class for a priority queue implemented using heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (float(priority), item))

    def get(self):
        return heapq.heappop(self.elements)[1]
