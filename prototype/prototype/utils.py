import os
import sys
import fcntl
import datetime
import collections
import heapq
import itertools


def debug_print(message, file=sys.stderr):
    print(f"[{datetime.datetime.now()}] {message}", file=file)


def atomic_row_write(file_path, entry):
    with open(file_path, "a") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(entry + "\n")
        fcntl.flock(file, fcntl.LOCK_UN)


def timestamped_process_id():
    pid = os.getpid()
    return f"{datetime.datetime.now()} PID{pid}"


class PriorityQueue:
    _REMOVED = 'removed'

    def __init__(self):
        self.heap = []
        self.lookup = {}
        self.counter = itertools.count()

    def __len__(self):
        return len(self.heap)

    def __contains__(self, item):
        return item in self.lookup

    def push(self, element, priority):
        if element in self.lookup:
            self._mark_removed(element)
        count = next(self.counter)
        entry = [priority, count, element]
        self.lookup[element] = entry
        heapq.heappush(self.heap, entry)

    def pop(self):
        while len(self.heap) > 0:
            priority, count, task = heapq.heappop(self.heap)
            if task is not self._REMOVED:
                del self.lookup[task]
                return task
        raise ValueError("pop(): queue empty")

    def get_priority(self, element):
        try:
            entry = self.lookup[element]
            return entry[0]
        except KeyError:
            return None

    def _mark_removed(self, element):
        entry = self.lookup.pop(element)
        entry[-1] = self._REMOVED


class FastLookupQueue:
    # TODO add lookup table

    def __init__(self):
        self.deque = collections.deque()

    def __len__(self):
        return len(self.deque)

    def __contains__(self, item):
        return item in self.deque

    def push_right(self, item):
        self.deque.append(item)

    def push_left(self, item):
        self.deque.appendleft(item)

    def pop_left(self):
        return self.deque.popleft()

    def pop_right(self):
        return self.deque.pop()
