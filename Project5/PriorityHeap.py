from typing import List, Tuple, Any


class Node:
    """
    Node definition should not be changed in any way
    """
    __slots__ = ['key', 'value']

    def __init__(self, k: Any, v: Any):
        """
        Initializes node
        :param k: key to be stored in the node
        :param v: value to be stored in the node
        """
        self.key = k
        self.value = v

    def __lt__(self, other):
        """
        Less than comparator
        :param other: second node to be compared to
        :return: True if the node is less than other, False if otherwise
        """
        return self.key < other.key or (self.key == other.key and self.value < other.value)

    def __gt__(self, other):
        """
        Greater than comparator
        :param other: second node to be compared to
        :return: True if the node is greater than other, False if otherwise
        """
        return self.key > other.key or (self.key == other.key and self.value > other.value)

    def __eq__(self, other):
        """
        Equality comparator
        :param other: second node to be compared to
        :return: True if the nodes are equal, False if otherwise
        """
        return self.key == other.key and self.value == other.value

    def __str__(self):
        """
        Converts node to a string
        :return: string representation of node
        """
        return '({0}, {1})'.format(self.key, self.value)

    __repr__ = __str__


class PriorityQueue:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = []

    def __str__(self) -> str:
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data)

    __repr__ = __str__

    def to_tree_format_string(self) -> str:
        """
        Prints heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""
        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self.data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def __len__(self) -> int:
        """
        return the length of self.data
        :return: len(self.data)
        """
        return len(self.data)

    def empty(self) -> bool:
        """
        check if self.data is empty, if is, return True. Else, return False
        :return: bool shows if self.data is empty
        """
        if len(self.data) == 0:
            return True
        return False

    def top(self) -> Node:
        """
        check if self.data is empty, if it's empty, return None
        else, return the top node in P_queue
        :return: top node in P_queue
        """
        if len(self.data) == 0:
            return None
        return self.data[0]

    def get_left_child_index(self, index: int) -> int:
        """
        get the node's left child's index in self.data
        :param index: the index of the node we are getting their left child
        :return: the index of node[index].left
        """
        if index * 2 + 1 < len(self.data):
            if self.data[index * 2 + 1] is not None:
                return index * 2 + 1
        return None

    def get_right_child_index(self, index: int) -> int:
        """
        get the node's right child's index in self.data
        :param index: the index of the node we are getting their right child
        :return: the index of node[index].right
        """
        if index * 2 + 2 < len(self.data):
            if self.data[index * 2 + 2] is not None:
                return index * 2 + 2
        return None

    def get_parent_index(self, index: int) -> int:
        """
        get the node's parent's index in self.data
        :param index: the index of the node we are getting it's parent
        :return: the index of node[index].parent
        """
        if len(self.data) > (index - 1) // 2 >= 0:
            if self.data[(index - 1) // 2] is not None:
                return (index - 1) // 2
        return None

    def push(self, key: Any, val: Any) -> None:
        """
        add node into p_queue
        :param key: the key of the node being add
        :param val: the value of the node being add
        :return: None
        """
        self.data.append(Node(key, val))
        self.percolate_up(len(self.data) - 1)

    def pop(self) -> Node:
        """
        remove the top node from p_queue
        :return: the node being removed
        """
        if self.empty():
            return None
        self.data[0], self.data[len(self.data) - 1] = self.data[len(self.data) - 1], self.data[0]
        item = self.data.pop()
        self.percolate_down(0)
        return item

    def get_min_child_index(self, index: int) -> int:
        """
        go through different cases and return the child with min value
        :param index: the index of node we are looking for the min_child
        :return: the index of min_child of self.data[index]
        """
        if self.empty():
            return None
        if self.get_left_child_index(index) is None and self.get_right_child_index(index) is None:
            return None
        if self.get_left_child_index(index) is not None and self.get_right_child_index(index) is None:
            return self.get_left_child_index(index)
        if self.get_left_child_index(index) is None and self.get_right_child_index(index) is not None:
            return self.get_right_child_index(index)
        left = self.get_left_child_index(index)
        right = self.get_right_child_index(index)
        if self.data[left] < self.data[right]:
            return left
        else:
            return right

    def percolate_up(self, index: int) -> None:
        """
        go through the tree from leaf node to root node and swap position if needed.
        :param index: the node we started from
        :return: None
        """
        parent = self.get_parent_index(index)
        if index > 0 and self.data[index] < self.data[parent]:
            self.data[index], self.data[parent] = self.data[parent], self.data[index]
            self.percolate_up(parent)

    def percolate_down(self, index: int) -> None:
        """
        go through the tree from root node to leaf node and swap position if needed.
        :param index: the root node
        :return: None
        """
        if self.get_left_child_index(index) is not None:
            left = self.get_left_child_index(index)
            small = left
            if self.get_right_child_index(index):
                right = self.get_right_child_index(index)
                if self.data[right] < self.data[left]:
                    small = right
            if self.data[small] < self.data[index]:
                self.data[index], self.data[small] = self.data[small], self.data[index]
                self.percolate_down(small)


class MaxHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = PriorityQueue()

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data.data)

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self.data)

    def print_tree_format(self):
        """
        Prints heap in bfs format
        """
        self.data.tree_format()

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def empty(self) -> bool:
        """
        check if self.data is empty, if is, return True. Else, return False
        :return: bool shows if self.data is empty
        """
        if self.data.empty():
            return True
        return False

    def top(self) -> int:
        """
        get the top node from max heap
        :return: the value of that top node in max_heap
        """
        if self.empty():
            return None
        top_node = self.data.top()
        value = top_node.value
        return -value

    def push(self, key: int) -> None:
        """
        add node into max_heap
        :param key: the key that's being add into max_heap
        :return: None
        """
        key = -key
        self.data.push(key, key)

    def pop(self) -> int:
        """
        delete the node on the top of the max_heap
        :return: the value of that node
        """
        if self.empty():
            return None
        popped = self.data.pop()
        value = popped.value
        return -value


def heap_sort(array):
    """
    use max_heap to sort the array inplace, use the first for loop to
    add all the value into the max_heap, then pop each one after being sorted
    in max_heap and set array[i] = -value because we push -data to make p_queue work like a max_heap
    :param array: the array we are sorting
    :return: sorted array
    """
    max_he = MaxHeap()
    for data in array:
        max_he.push(-data)

    for i in range(len(array)):
        value = max_he.pop()
        array[i] = -value
    return array


def find_ranking(rank, results: List[Tuple[int, str]]) -> str:
    """
    create a p_queue to store every element in results, then pop the p_queue
    until we pop as many times as the rank, then return the name of that team
    :param rank: the ranking for results and return
    :param results: a list of tuple with lose count and name
    :return: the team name in rank
    """
    name = ''
    queue = PriorityQueue()
    for each in results:
        queue.push(each[0], each[1])

    for i in range(rank):
        nodes = queue.pop()
        if nodes is None:
            return None
        name = nodes.value
    return name
