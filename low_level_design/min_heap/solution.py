class MinHeap:

    def __init__(self):
        self.min_heap = []

    def _parent(self, idx:int):
        return (idx-1)//2

    def _left_child(self, idx: int):
        return 2*idx + 1

    def _right_child(self, idx:int):
        return 2*idx + 2
    
    def _swap(self, parent_idx: int, child_idx:int):
        self.min_heap[parent_idx], self.min_heap[child_idx] = self.min_heap[child_idx], self.min_heap[parent_idx]

    def push(self, val: int):
        self.min_heap.append(val)
        val_idx = len(self.min_heap)-1
        while val_idx > 0:
            parent_idx = self._parent(val_idx)
            if self.min_heap[parent_idx] <= self.min_heap[val_idx]:
                break
            self._swap(parent_idx, val_idx)
            val_idx = parent_idx


    def delete(self):

        if not self.min_heap:
            return None
        
        # for len == 1, self.min_heap[0] = self.min_heap.pop() won't work and give us IndexError 
        if len(self.min_heap) == 1:
            return self.min_heap.pop()

        parent_idx = 0

        min_val = self.min_heap[0]


        self.min_heap[0] = self.min_heap.pop()

        while True:
            lc_idx = self._left_child(parent_idx)
            rc_idx = self._right_child(parent_idx)

            # lc_idx, rc_idx are providing a number which can be greater than len(self.min_heap)
            if lc_idx >= len(self.min_heap):
                break
            
            # assume lc_idx as smaller_child_idx, compare and update
            smaller_child_idx = lc_idx

            if rc_idx < len(self.min_heap) and self.min_heap[rc_idx] < self.min_heap[lc_idx]:
                smaller_child_idx = rc_idx
            # already min heap
            if self.min_heap[parent_idx] <= self.min_heap[smaller_child_idx]:
                break

            self._swap(parent_idx, smaller_child_idx)
            parent_idx = smaller_child_idx
        return min_val

    def get_min_val(self):
        return self.min_heap[0]
    
    def __len__(self):
        return len(self.min_heap)
    
    def __str__(self):
        return str(self.min_heap)
    

if __name__ == "__main__":
    min_heap = MinHeap()
    lst = [8, 6, 3, 10, 11]
    for ele in lst:
        min_heap.push(ele)
        print(f"length : {len(min_heap)}")
    print(f"MinHeap : {min_heap}")
    for i in range(len(lst)):
        print(min_heap.delete())
