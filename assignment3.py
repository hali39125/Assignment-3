
import random


# ============================================================
# PART 1: QUICKSORT
# ============================================================

def partition_first(arr, low, high):
    """Partition using the first element as the pivot."""
    pivot = arr[low]
    i = low

    for j in range(low + 1, high + 1):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[low], arr[i] = arr[i], arr[low]
    return i


def deterministic_quicksort(values):
    """
    First-element-pivot Quicksort.
    Returns a sorted copy and uses an explicit stack.
    """
    arr = list(values)

    if len(arr) < 2:
        return arr

    stack = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()

        while low < high:
            pivot_index = partition_first(arr, low, high)

            # Process the smaller partition immediately.
            if pivot_index - low < high - pivot_index:
                if pivot_index + 1 < high:
                    stack.append((pivot_index + 1, high))
                high = pivot_index - 1
            else:
                if low < pivot_index - 1:
                    stack.append((low, pivot_index - 1))
                low = pivot_index + 1

    return arr


def partition_random(arr, low, high, rng):
    """Choose a uniformly random pivot from the current subarray."""
    pivot_index = rng.randrange(low, high + 1)
    arr[low], arr[pivot_index] = arr[pivot_index], arr[low]
    return partition_first(arr, low, high)


def randomized_quicksort(values, seed=None):
    """
    Randomized Quicksort.
    Selects a uniformly random pivot for each partition.
    Returns a sorted copy.
    """
    arr = list(values)

    if len(arr) < 2:
        return arr

    rng = random.Random(seed)
    stack = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()

        while low < high:
            pivot_index = partition_random(arr, low, high, rng)

            if pivot_index - low < high - pivot_index:
                if pivot_index + 1 < high:
                    stack.append((pivot_index + 1, high))
                high = pivot_index - 1
            else:
                if low < pivot_index - 1:
                    stack.append((low, pivot_index - 1))
                low = pivot_index + 1

    return arr


# ============================================================
# PART 2: HASH TABLE WITH CHAINING
# ============================================================

class ChainedHashTable:
    """
    Hash table using separate chaining.

    Integer keys use a universal-family-style hash:
        h(k) = ((a*k + b) mod p) mod capacity

    p is prime, a is in [1, p-1], and b is in [0, p-1].
    """

    PRIME = 2_147_483_647

    def __init__(self, capacity=8, max_load_factor=0.75, seed=None):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        if max_load_factor <= 0:
            raise ValueError("Load factor threshold must be positive.")

        self.capacity = capacity
        self.max_load_factor = max_load_factor
        self.size = 0

        rng = random.Random(seed)
        self.a = rng.randrange(1, self.PRIME)
        self.b = rng.randrange(0, self.PRIME)

        self.buckets = [[] for _ in range(capacity)]

    @property
    def load_factor(self):
        return self.size / self.capacity

    def _hash(self, key):
        k = key if isinstance(key, int) else hash(key)
        return ((self.a * (k % self.PRIME) + self.b)
                % self.PRIME) % self.capacity

    def _resize(self, new_capacity):
        """Rebuild buckets and redistribute all existing entries."""
        entries = [
            item
            for bucket in self.buckets
            for item in bucket
        ]

        self.capacity = new_capacity
        self.buckets = [[] for _ in range(self.capacity)]

        for key, value in entries:
            self.buckets[self._hash(key)].append((key, value))

    def insert(self, key, value):
        """Insert a key-value pair or update an existing key."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.load_factor > self.max_load_factor:
            self._resize(self.capacity * 2)

    def search(self, key):
        """Return the associated value, or None if absent."""
        index = self._hash(key)

        for existing_key, value in self.buckets[index]:
            if existing_key == key:
                return value

        return None

    def delete(self, key):
        """Delete a key and return True; return False if absent."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self.size -= 1
                return True

        return False

    def __len__(self):
        return self.size


# ============================================================
# BASIC TESTS
# ============================================================

def run_tests():
    test_cases = [
        [],
        [1],
        [5, 2, 8, 1, 3],
        list(range(100)),
        list(range(100, 0, -1)),
        [7] * 100,
        [3, 1, 3, 2, 1, 2, 3],
    ]

    for values in test_cases:
        expected = sorted(values)

        assert deterministic_quicksort(values) == expected
        assert randomized_quicksort(values, seed=42) == expected

    table = ChainedHashTable(seed=42)

    table.insert("apple", 10)
    table.insert("banana", 20)

    assert table.search("apple") == 10
    assert table.search("missing") is None

    table.insert("apple", 99)
    assert table.search("apple") == 99
    assert len(table) == 2

    assert table.delete("banana") is True
    assert table.search("banana") is None
    assert table.delete("missing") is False

    for i in range(200):
        table.insert(i, i * i)

    for i in range(200):
        assert table.search(i) == i * i

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()