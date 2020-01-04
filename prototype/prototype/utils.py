import os
import sys
import fcntl
import datetime
import collections
import heapq
import itertools


def debug_print(message, file=sys.stderr):
    """
    Prints a message with a timestamp.
    """
    print(f"[{datetime.datetime.now()}] {message}", file=file)


def atomic_row_write(file_path, entry):
    """
    Atomically writes to a file, useful for multiple processes.
    """
    with open(file_path, "a") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(entry + "\n")
        fcntl.flock(file, fcntl.LOCK_UN)


def timestamped_process_id():
    """
    Returns an identifier of the process.
    """
    pid = os.getpid()
    return f"{datetime.datetime.now()} PID{pid}"


class PriorityQueue:
    """
    A priority queue. Always pops the element with the LOWEST priority.
    """
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
        """
        Pushes an element to the queue.
        """
        if element in self.lookup:
            self._mark_removed(element)
        count = next(self.counter)
        entry = [priority, count, element]
        self.lookup[element] = entry
        heapq.heappush(self.heap, entry)

    def pop(self):
        """
        Pops the element with the lowest priority.
        """
        while len(self.heap) > 0:
            priority, count, task = heapq.heappop(self.heap)
            if task is not self._REMOVED:
                del self.lookup[task]
                return task
        raise ValueError("pop(): queue empty")

    def get_priority(self, element):
        """
        Returns the priority of an element, or None if not present in the queue.
        """
        try:
            entry = self.lookup[element]
            return entry[0]
        except KeyError:
            return None

    def _mark_removed(self, element):
        entry = self.lookup.pop(element)
        entry[-1] = self._REMOVED


class Multiset:
    """
    A multiset (a set which can store the same item several times).
    """
    def __init__(self):
        self.values = {}

    def __len__(self):
        return len(self.values)

    def __contains__(self, item):
        return item in self.values.keys()

    def insert(self, item):
        """
        Adds an item into the multiset.
        """
        if item in self.values:
            self.values[item] = self.values[item] + 1
        else:
            self.values[item] = 1

    def remove(self, item):
        """
        Removes a SINGLE item once from the multiset.
        """
        if item in self.values.keys():
            if self.values[item] > 1:
                self.values[item] = self.values[item] - 1
            else:
                del self.values[item]
        else:
            raise KeyError(str(item))

    def get(self, item):
        """
        Gets the value of the item in the multiset. Useful if item is not totally equal.
        """
        for key in self.values.keys():
            if key == item:
                return key
        else:
            raise KeyError(str(item))


class FastLookupQueue:
    """
    A queue which can quickly determine whether an item is enqueued.
    """

    def __init__(self):
        self.deque = collections.deque()
        self.lookup = Multiset()

    def __len__(self):
        return len(self.deque)

    def __contains__(self, item):
        return item in self.lookup

    def get(self, item):
        """
        Returns the value of the item in the queue. Useful if item is not totally equal.
        """
        return self.lookup.get(item)

    def push_right(self, item):
        self.deque.append(item)
        self.lookup.insert(item)

    def push_left(self, item):
        self.deque.appendleft(item)
        self.lookup.insert(item)

    def pop_left(self):
        item = self.deque.popleft()
        self.lookup.remove(item)
        return item

    def pop_right(self):
        item = self.deque.pop()
        self.lookup.remove(item)
        return item
