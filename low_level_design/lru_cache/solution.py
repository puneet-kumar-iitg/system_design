class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

        self.head = Node(None, None)
        self.tail = Node(None, None)

        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        head_next = self.head.next
        self.head.next = node
        node.next = head_next
        node.prev = self.head
        head_next.prev = node


    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache.get(key)

        self._remove(node)
        self._add_to_head(node)
        return node.val


    def put(self, key, val):
        if key in self.cache:
            node = self.cache.get(key)
            node.val = val

            # remove current accessed node
            # add current access node to head
            self._remove(node)
            self._add_to_head(node)
            return None
        
        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev
            # remove current accessed node
            self._remove(lru_node)
            del self.cache[lru_node.key] # self.cache.pop(key, None)

        node = Node(key, val)
        self.cache[key] = node

        self._add_to_head(node)


if __name__ == "__main__":
    lru = LRUCache(capacity=3)
    lru.put("A", 1)
    lru.put("B", 2)
    print(lru.get("A"))
    lru.put("C", 3)
    lru.put("D", 4)
    print(lru.get("A"))
    print(lru.get("D"))
    lru.put("E", 5)
    print(lru.get("B"))

