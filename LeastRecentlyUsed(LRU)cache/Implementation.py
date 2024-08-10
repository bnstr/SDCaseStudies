# Least Recently Used (LRU) cache.
#
# Implement the LRUCache class:
#
# LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
# int get(int key) Return the value of the key if the key exists, otherwise return -1.
# void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache.
# If the number of keys exceeds the capacity from this operation, evict the least recently used key.
# The functions get and put must each run in O(1) average time complexity.

# data modeling , for ,
# cache capacity=2  --> LRUCache(2)
# cache.put(1, 1) -->      items=[(1: 1)]
# cache.put(2, 2) -->      items=[(2: 2), (1: 1)]
# cache.put(3, 3) -->      items=[(3: 3), (2: 2)]    # (1: 1) was evicted
# cache.get(1)    -->      -1                        # 1 was evicted when 3 was added
# cache.put(2, 10)   --> items=[(2: 2), (3: 3)]      # Update value will move to head (most recent)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Hashmap to store key-node pairs
        self.head = Node(0, 0)  # Dummy head node
        self.tail = Node(0, 0)  # Dummy tail node
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node):
        """Add a node right after the head."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)  # Move the accessed node to the head
            return node.value
        return -1

    def put(self, key: int, value: int):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            # Remove the least recently used node
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

    def __repr__(self) -> str:
        # Create a list to store the string representations of the key-value pairs
        items = []
        current = self.head.next
        while current != self.tail:
            items.append(f"({current.key}: {current.value})")
            current = current.next
        return f"LRUCache(capacity={self.capacity}, items=[{', '.join(items)}])"


import unittest
class LRUTests(unittest.TestCase):

    def setUp(self):
        # Initialize LRUCache with a capacity of 2
        self.cache = LRUCache(2)

    def test_put_and_get(self):
        # Test adding and retrieving elements
        self.cache.put(1, 1)
        self.assertEqual(self.cache.get(1), 1, "get(1) failed to return the correct value")
        self.cache.put(2, 2)
        self.assertEqual(self.cache.get(2), 2, "get(2) failed to return the correct value")

    def test_eviction_policy(self):
        # Test that the cache evicts the least recently used item
        self.cache.put(1, 1)
        print(f"\n\ntest_eviction_policy")
        print(f"put 1:1 to cache, {self.cache} ")
        self.cache.put(2, 2)
        print(f"put 2:2 to cache, {self.cache} ")
        self.cache.put(3, 3)  # This should evict key 1
        print(f"put 3:3 to cache, {self.cache} ")
        print(f"the lru: 1:1  was evicted, {self.cache} ")
        print(f"get cache.get(1) returns:, {self.cache.get(1)} ")
        self.assertEqual(self.cache.get(1), -1, "get(1) should return -1 after eviction")
        self.assertEqual(self.cache.get(2), 2, "get(2) failed to return the correct value")
        self.assertEqual(self.cache.get(3), 3, "get(3) failed to return the correct value")

    def test_update_existing_key(self):
        # Test updating the value of an existing key and ensuring it updates correctly
        self.cache.put(1, 1)
        print(f"\n\ntest_update_existing_key")
        print(f"put 1:1 to cache, {self.cache} ")
        self.cache.put(2, 2)
        print(f"put 2:2 to cache, {self.cache} ")
        self.cache.put(1, 10)  # Update value of key 1
        print(f"update value of 1 to 10 moves 1 on TOP, put(1:10), {self.cache} ")
        self.assertEqual(self.cache.get(1), 10, "get(1) failed to return the updated value")

    def test_peek_and_next_alternate_returns_correct_value(self):
        # Test accessing elements and their order
        self.cache.put(1, 1)
        self.assertEqual(self.cache.get(1), 1, "get(1) failed to return the correct value")
        self.cache.put(2, 2)
        self.assertEqual(self.cache.get(2), 2, "get(2) failed to return the correct value")
        self.cache.put(3, 3)  # This should evict key 1
        self.assertEqual(self.cache.get(1), -1, "get(1) should return -1 after eviction")
        self.assertEqual(self.cache.get(2), 2, "get(2) failed to return the correct value")
        self.assertEqual(self.cache.get(3), 3, "get(3) failed to return the correct value")

    def test_capacity_edge_case(self):
        # Test the edge case where the cache capacity is 1
        cache = LRUCache(1)
        print(f"\n\ntest_capacity_edge_case")
        print(f"capacity is 1, {cache} ")
        cache.put(1, 1)
        print(f"put 1:1 to cache, {cache} ")
        self.assertEqual(cache.get(1), 1, "get(1) failed to return the correct value")
        cache.put(2, 2)  # This should evict key 1
        print(f"put 2:2 to cache, evicted  1:1 {cache}  ")
        self.assertEqual(cache.get(1), -1, "get(1) should return -1 after eviction")
        self.assertEqual(cache.get(2), 2, "get(2) failed to return the correct value")

if __name__ == "__main__":
    unittest.main()