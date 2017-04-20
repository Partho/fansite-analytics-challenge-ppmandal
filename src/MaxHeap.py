
# Class to maintain Max-heap

import heapq

class MaxHeap:
    def __init__(self):
        # There is no max-heap implementation in Python's standard library
        # So it is based on min-heap with storing negative values
        self.max_heap = []

        # List to store top-k result
        self.result = []

    def add(self, key, value):
        # Store the key, value pair in max heap
        heapq.heappush(self.max_heap, (-value, key))

    # Extract top-k elements in heap
    # O(n + klogn) time complexity
    # where n is elements in self.max_heap
    def extract_k_largest(self, k):
        while self.max_heap and k > 0:
            item = heapq.heappop(self.max_heap)
            if len(item)==2:
                self.result.append((item[1], -item[0]))
            else:
                self.result.append(item[1])
            k -= 1
        return self.result
