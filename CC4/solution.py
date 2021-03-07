"""
Name: Che-Jui (Jerry), Chang
CC4 - Starter Code
CSE 331 Fall 2020
Professor Sebnem Onsay
"""


# You must add insert(), remove() and shortest_book() as defined by the specs.
# Don't forget docstrings!
class Books:
    """books has attribute pile and min. Both are lists.
    The pile will store all the books that's being inserted.
    The min will store the smallest book in the last element.
    We creates insert(), remove(), and shortest_book() functions
    in order to allow test cases to work.
    """
    def __init__(self):
        """Create an attribute call pile as a list,
        another attribute call min.
        Min is a list to store the smallest int we find
        in the last element of the list."""
        self.pile = []
        self.min = []

    def insert(self, book):
        """Insert the book into the pile. If book is
        smaller than the last element of the min list,
        we add the book into the back of the min list."""
        self.pile.append(book)
        if not self.min or book <= self.shortest_book():
            self.min.append(book)

    def remove(self):
        """Check if the pile is empty. If true, return None.
        Else, we remove the last element in pile.
        If the element that was removed is the smallest,
        we also remove it from the min list and return the
        pages of the book that's being removed."""
        if len(self.pile) == 0:
            return None
        last = self.pile.pop()
        if last == self.shortest_book():
            self.min.pop()
        return last

    def shortest_book(self):
        """Check if the pile if empty. If true, return None.
        Else, we return the last element in the min list."""
        if len(self.min) == 0:
            return None
        return self.min[-1]
