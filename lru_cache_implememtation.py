"""
==============================
Problem 1: LRU Cache
==============================
To achieve O(1) for both get and put, I use two data structures together:

1. A HashMap (Python dict): maps each key directly to its node in the
  linked list. This gives O(1) lookup — no searching required.

2. A Doubly Linked List: maintains the order of use. The HEAD end holds
    the most recently used item; the TAIL end holds the least recently used.
    Because each node has both a prev and next pointer, we can remove any
    node from the middle of the list in O(1) — no shifting required.

Neither structure alone achieves O(1) for everything:
   - A HashMap alone has no concept of order.
   - A Linked List alone requires O(n) to search for a key.
Together, the HashMap handles fast lookup and the Linked List handles
fast ordering/eviction.

"""
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = next

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} #HashMap: Key -> Node

        self.head = Node(0,0)
        self.tail = Node(0,0) 
        self.head.next = self.tail
        self.tail.prev = self.head

    
    # Helper
    def _remove(self, node:Node):
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    
    def _insert_at_front(self, node:Node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    
    def get(self, key:int)-> int:

        """
        Return the value for key, or -1 if not found.
        Also marks the key as most recently used.
        Time: O(1)

        """
        if key not in self.cache:
            return -1
        node = self.cache[key]

        # move to front to mark as recently used
        self._remove(node)
        self._insert_at_front(node)
        return node.value
    
    def put(self, key:int, value:int)-> None:
        """
        Insert or update key-value pair.
        Evicts the least recently used item if over capacity.
        Time: O(1)

        """
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self._insert_at_front(node) #most recently used

        if len(self.cache)>self.capacity:
            lru_node = self.tail.prev #LRU
            self._remove(lru_node)
            del self.cache[lru_node.key] # performing LRU and removing that least used from hashmap


# --- Quick smoke test ---
cache = LRUCache(2)
cache.put(1, 1)   # cache: {1=1}
cache.put(2, 2)   # cache: {1=1, 2=2}
print(cache.get(1))    # returns 1  — key 1 is now most recent
cache.put(3, 3)   # capacity hit — evicts key 2 (least recent)
print(cache.get(2))    # returns -1 — key 2 was evicted
cache.put(4, 4)   # evicts key 1
print(cache.get(1))    # returns -1
print(cache.get(3))    # returns 3
print(cache.get(4))    # returns 4

        

