# Standard library import
import collections
import itertools
import heapq


class PairPriorityQueue(object):

    def __init__(self):
        # list of entries arranged in a heap
        self._pq = []

        # mapping of tasks to entries
        self.pairs = collections.defaultdict(dict)

        # unique sequence count
        self._counter = itertools.count()

    def add_pair(self, v0, v1, priority):
        if v0 in self.pairs and v1 in self.pairs[v0]:
            self.remove_pair(v0, v1)
        key = sorted([v0, v1])
        count = next(self._counter)
        entry = [priority, count, key[0], key[1], False]
        self.pairs[v0][v1] = entry
        self.pairs[v1][v0] = entry

    def remove_pair(self, v0, v1):
        entry = self.pairs[v0].pop(v1)
        del self.pairs[v1][v0]
        entry[-1] = True

    def get_pairs(self, v0):
        return list(self.pairs[v0].keys())

    def pop_pair(self):
        pq, pairs = self._pq, self.pairs
        heappop = heapq.heappop
        while pq:
            priority, count, v0, v1, removed = heappop(pq)
            if not removed:
                del pairs[v0][v1]
                del pairs[v1][v0]
                return v0, v1
        raise KeyError('pop from an empty priority queue')

# def add_task(task, priority=0):
#     'Add a new task or update the priority of an existing task'
#     if task in entry_finder:
#         remove_task(task)
#     count = next(counter)
#     entry = [priority, count, task]
#     entry_finder[task] = entry
#     heapq.heappush(pq, entry)
#
#
# def remove_task(task):
#     'Mark an existing task as REMOVED.  Raise KeyError if not found.'
#     entry = entry_finder.pop(task)
#     entry[-1] = REMOVED
#
#
# def pop_task():
#     'Remove and return the lowest priority task. Raise KeyError if empty.'
#     while pq:
#         priority, count, task = heapq.heappop(pq)
#         if task is not REMOVED:
#             del entry_finder[task]
#             return task
#     raise KeyError('pop from an empty priority queue')