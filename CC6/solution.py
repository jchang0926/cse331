"""
CC6 - It's As Easy As 01-10-11
Name: Che-Jui (Jerry), Chang
"""

from typing import Generator, Any


class Node:
    """
    Node Class
    :value: stored value
    :next: reference to next node
    """

    def __init__(self, value) -> None:
        """
        Initializes the Node class
        """
        self.value: str = value
        self.next: Node = None
    def __str__(self) -> str:
        """
        Returns string representation of a Node
		"""

        return self.value


class Queue:
    """
    Queue Class
    :first: reference to first node in the queue
    :last: reference to last node in the queue
    """

    def __init__(self) -> None:
        """
        Initializes the Queue class
        """
        self.first: Node = None
        self.last: Node = None

    def __str__(self) -> str:
        final = 'front - '
        current = self.first
        while current is not None:
            final += str(current) + ' - '
            current = current.next
        final += "last"
        return final

    def insert(self, value: str) -> None:
        """
        insert the node at the end of the queue
        :param value: the value for the node
        :return: None
        """
        new_node = Node(value)
        if self.first is None:
            self.first = new_node
        else:
            self.last.next = new_node
        self.last = new_node

    def pop(self) -> str:
        """
        remove the first element in queue and reset the attributes
        :return: the value that's being pop
        """
        if self.first is None:
            return None
        ans = self.first.value
        new_head = self.first.next
        self.first = new_head
        if self.first is None:
            self.last = None
        return ans


def alien_communicator(n: Any) -> Generator[str, None, None]:
    """
    check the input n is a int and bigger than -1.
    if true for these two conditions, we yield the binary value from 0 to n
    :param n: number counts
    :return: yield the binary value
    """
    if type(n) == int and n >= 0:
        out = Queue()
        out.insert('1')
        yield '0'
        count = 0
        while count < n:
            first = str(out.pop())
            out.insert(first + '0')
            out.insert(first + '1')
            count += 1
            yield first
    else:
        return
