"""
Your Name: Che-Jui (Jerry), Chang
Project 4 - Tries
CSE 331 Fall 2020
Professor Sebnem Onsay
"""

from __future__ import annotations
from typing import Tuple, Dict, List


class TrieNode:
    """
    Implementation of a trie node.
    """

    # DO NOT MODIFY

    __slots__ = "children", "is_end"

    def __init__(self, arr_size: int = 26) -> None:
        """
        Constructs a TrieNode with arr_size slots for child nodes.
        :param arr_size: Number of slots to allocate for child nodes.
        :return: None
        """
        self.children = [None] * arr_size
        self.is_end = 0

    def __str__(self) -> str:
        """
        Represents a TrieNode as a string.
        :return: String representation of a TrieNode.
        """
        if self.empty():
            return "..."
        children = self.children  # to shorten proceeding line
        return str({chr(i + ord("a")) + "*"*min(children[i].is_end, 1): children[i] for i in range(26) if children[i]})

    def __repr__(self) -> str:
        """
        Represents a TrieNode as a string.
        :return: String representation of a TrieNode.
        """
        return self.__str__()

    def __eq__(self, other: TrieNode) -> bool:
        """
        Compares two TrieNodes for equality.
        :return: True if two TrieNodes are equal, else False
        """
        if not other or self.is_end != other.is_end:
            return False
        return self.children == other.children

    # Implement Below

    def empty(self) -> bool:
        """
        check if the node has child or not.
        if no, return True
        else, return False
        :return: bool of if the node has child or not.
        """
        if self.children != 26*[None]:
            return False
        return True

    @staticmethod
    def _get_index(char: str) -> int:
        """
        take a character and make it lower case,
        then return the character's index by getting
        the ASCII value - 'a' to get the index.
        :param char: a character
        :return: the index of that character by alphabetical order.
        """
        if char.isupper():
            char = char.lower()
        if char.islower():
            return ord(char) - ord('a')

    def get_child(self, char: str) -> TrieNode:
        """
        if the node has child, we get the index of char by calling _get_index(char)
        then return the children list[index]
        :param char: a character
        :return: pointer of the self.child[index]
        """
        if self.empty():
            return None
        index = self._get_index(char)
        return self.children[index]

    def set_child(self, char: str) -> None:
        """
        get the index of character by calling _get_index(char)
        then set the self.children[index] = Trienode()
        :param char: the character we want self.children to create a new node
        :return: None
        """
        index = self._get_index(char)
        self.children[index] = TrieNode()

    def delete_child(self, char: str) -> None:
        """
        get the index of character by calling _get_index(char)
        then set the self.children[index] = None
        :param char: the character we want self.children to delete
        :return: None
        """
        index = self._get_index(char)
        self.children[index] = None


class Trie:
    """
    Implementation of a trie.
    """

    # DO NOT MODIFY

    __slots__ = "root", "unique", "size"

    def __init__(self) -> None:
        """
        Constructs an empty Trie.
        :return: None.
        """
        self.root = TrieNode()
        self.unique = 0
        self.size = 0

    def __str__(self) -> str:
        """
        Represents a Trie as a string.
        :return: String representation of a Trie.
        """
        return "Trie Visual:\n" + str(self.root)

    def __repr__(self) -> str:
        """
        Represents a Trie as a string.
        :return: String representation of a Trie.
        """
        return self.__str__()

    def __eq__(self, other: Trie) -> bool:
        """
        Compares two Tries for equality.
        :return: True if two Tries are equal, else False
        """
        return self.root == other.root

    # Implement Below

    def add(self, word: str) -> int:
        """
        add words into the trie by calling the inner function recursively.
        :param word: the word that's going to get added into the trie
        :return: the count of that words in the trie
        """
        def add_inner(node: TrieNode, index: int) -> int:
            """
            the recursive function to get deeper into the trie to add each character.
            if node.get_child(word[index]) is not None, we don't add a new child because it already existed
            :param node: the node that's going to get a child
            :param index: the index of word from the outer function
            :return: the count of the word that's in the trie
            """
            if index < len(word):
                if node.get_child(word[index]) is None:
                    node.set_child(word[index])
                index += 1
                return add_inner(node.get_child(word[index-1]), index)
            else:
                node.is_end += 1
                return node.is_end
        index = 0
        out = add_inner(self.root, index)
        if out == 1:
            self.unique += 1
        self.size += 1
        return out

    def search(self, word: str) -> int:
        """
        check if the word exist in trie by calling the inner
        function recursively to check each word[index].
        return the count of the word in trie.
        :param word: the word we are looking for in trie
        :return: the count of the word
        """
        def search_inner(node: TrieNode, index: int) -> int:
            """
            the recursive function to get deeper into the trie to search each character.
            if node.get_child(word[index]) is not None, we keep going into the trie to find the word.
            :param node: the node that's in the word[index - 1] in order to check the child.
            :param index: the index of word from outer function
            :return: the count of that word being added into this trie
            """
            if index < len(word):
                if node.get_child(word[index]) is not None:
                    index += 1
                    return search_inner(node.get_child(word[index-1]), index)
                else:
                    return 0
            else:
                return node.is_end
        index = 0
        out = search_inner(self.root, index)
        return out

    def delete(self, word: str) -> int:
        """
        delete the words in trie by calling the inner function to get deeper into the trie.
        needs to check if each node needs to be prune or not.
        we delete nodes after we travel all the way to the end of the words, then delete them from
        their parents (the word[index - 1])
        :param word: the word we are deleting from trie
        :return: how many times does that word was added into the trie
        """
        def delete_inner(node: TrieNode, index: int) -> Tuple[int, bool]:
            """
            the recursive function to get deeper into the trie to delete the words.
            when we are at the last character of the word, we check if the node.child is empty.
            if it is, we return node.is_end, True as a tuple. else, return node.is_end, False.
            When we call this function recursively, we need two variable to catch the count and bool that's returned
            if the bool is True, we do node.delete_child(word[index-1]) to delete the node.
            :param node: the node that's in the word[index - 1] in order to get the child.
            :param index: the index of word from the outer function
            :return: tuple of the last node.is_end and bool to check if we need to prune the node.
            """
            if index < len(word):
                if node.get_child(word[index]) is not None:
                    index += 1
                    count, remove_bool = delete_inner(node.get_child(word[index - 1]), index)
                    if remove_bool is True:
                        node.delete_child(word[index-1])
                    if node.is_end > 0 or not node.empty():
                        remove_bool = False
                    else:
                        remove_bool = True
                    return count, remove_bool
                else:
                    return 0, False
            else:
                if node.empty():
                    count = node.is_end
                    node.is_end = 0
                    return count, True
                else:
                    count = node.is_end
                    node.is_end = 0
                    return count, False
        index = 0
        times, check = delete_inner(self.root, index)
        if times != 0:
            self.unique -= 1
        self.size = self.size - times
        return times

    def __len__(self) -> int:
        """
        get the size of the Trie
        :return: size of the trie
        """
        return self.size

    def __contains__(self, word: str) -> bool:
        """
        if the word is in trie by calling self.search(word)
        if that's bigger than 0, return True. Else, return False
        :param word: the word we are looking for in the trie
        :return: bool of if the word is in the trie.
        """
        if self.search(word) > 0:
            return True
        return False

    def empty(self) -> bool:
        """
        if the trie has no child, return True
        else, return False
        :return: bool of if the trie has no child
        """
        if self.root.empty():
            return True
        return False

    def get_vocabulary(self, prefix: str = "") -> Dict[str, int]:
        """
        by giving a prefix, we need to get all the words with same prefix and same length in a dictionary.
        :param prefix: if prefix is "", we need to get all the words from trie.
        otherwise, we need to return words start with prefix
        :return: a dictionary of words as key and count as value.
        """
        def get_vocabulary_inner(node, suffix):
            """
            if node has no child, we check if node.is_end > 0.
            if it is, we add the word into dictionary
            if node has child, we go through each index in self.children to see
            which character exist in self.children.
            if the node.is_end > 0, we add the words and count into dictionary first,
            then we keep adding on the words and get the child of that character
            and call get_vocabulary_inner recursively.
            :param node: the node that exist in previous node.children
            :param suffix: characters we travel through.
            :return: None
            """
            if node.empty():
                if node.is_end > 0:
                    master[suffix] = node.is_end
                return
            for i in range(len(node.children)):
                if node.children[i] is not None:
                    if node.is_end != 0:
                        master[suffix] = node.is_end
                    new_suffix = suffix + chr(i + 97)
                    new_node = node.get_child(chr(i + 97))
                    get_vocabulary_inner(new_node, new_suffix)
        master = {}
        if prefix == '':
            get_vocabulary_inner(self.root, prefix)
        else:
            node = self.root
            for i in range(len(prefix)):
                if node.get_child(prefix[i]) is not None:
                    node = node.get_child(prefix[i])
                else:
                    return master
            get_vocabulary_inner(node, prefix)
        return master

    def autocomplete(self, word: str) -> Dict[str, int]:
        """
        the input is going to be a word or words with dots.
        whenever we see a dot, we need to check every kids that's not None
        at the previous node. Return the words with count that match the
        length of word and the format.
        :param word: words that we are looking for inside the trie.
                    if that words include dot, that means we need to get all
                    the possible words and check if the length of those
                    possible words. if it match those conditions, we add it into
                    the dictionary.
        :return: dictionary with words with key and count as value
        """
        def autocomplete_inner(node, prefix, index):
            """
            the recursive function that gets the child of node.
            we keep checking if the index is smaller than the len(word) from outer function.
            if len(word) == index, we check if that node.is_end is 0 or not.
            if node.is_end is 0, we just return.
            if node.is_end isn't 0, we add the prefix into the dictionary where predix is key,
            count is the value.
            :param node: starts with self.root. if node.children[i] is not None,
                        update the prefix and call this function with node.get_child(chr(i+97))
                        to get the other child
            :param prefix: the words we went through
            :param index: the index of the words
            :return: None
            """
            if index < len(word) and word[index] == '.':
                for i in range(len(node.children)):
                    if node.children[i] is not None:
                        new_prefix = prefix + chr(i + 97)
                        new_node = node.get_child(chr(i+97))
                        autocomplete_inner(new_node, new_prefix, index+1)
            elif index < len(word) and word[index] != '.':
                if node.get_child(word[index]) is not None:
                    new_prefix = prefix + word[index]
                    new_node = node.get_child(word[index])
                    autocomplete_inner(new_node, new_prefix, index + 1)
            else:
                if node.is_end == 0:
                    return
                else:
                    master[prefix] = node.is_end
                    return
        master = {}
        autocomplete_inner(self.root, '', 0)
        return master


class TrieClassifier:
    """
    Implementation of a trie-based text classifier.
    """

    # DO NOT MODIFY

    __slots__ = "tries"

    def __init__(self, classes: List[str]) -> None:
        """
        Constructs a TrieClassifier with specified classes.
        :param classes: List of possible class labels of training and testing data.
        :return: None.
        """
        self.tries = {}
        for cls in classes:
            self.tries[cls] = Trie()

    @staticmethod
    def accuracy(labels: List[str], predictions: List[str]) -> float:
        """
        Computes the proportion of predictions that match labels.
        :param labels: List of strings corresponding to correct class labels.
        :param predictions: List of strings corresponding to predicted class labels.
        :return: Float proportion of correct labels.
        """
        correct = sum([1 if label == prediction else 0 for label, prediction in zip(labels, predictions)])
        return correct / len(labels)

    # Implement Below

    def fit(self, class_strings: Dict[str, List[str]]) -> None:
        """
        we get the dictionary from input, we loop through each items and the words_list
        we loop through len(words_list) and split each list. then split the word_list[i]
        and check the each index is smaller than len(each).
        if index is less then len(each), we add the word[index].
        else, set index = 0
        :param class_strings: dictionary with class as key, training words as value
        :return: None
        """
        index = 0
        for name, words_lst in class_strings.items():
            for i in range(len(words_lst)):
                each = words_lst[i].split()
                while index < len(each):
                    self.tries[name].add(each[index])
                    index += 1
                index = 0

    def predict(self, strings: List[str]) -> List[str]:
        """
        predict each sentence belong to which class in the self.trie
        by getting each index, then looping through each class name in self.trie,
        then get each word from the first for loop and check each class's score.
        if the score is higher than highest, we make temp = name and set the highest = final
        append the name at temp into the prediction list and return the list when it's done.
        :param strings: the words we are comparing the score
        :return: a list with the highest score of class's name.
        """
        prediction = []
        temp = ''
        score = 0
        highest = -10
        for str_i in range(len(strings)):
            for name in self.tries.keys():
                for word_i in strings[str_i].split():
                    score += self.tries[name].search(word_i)
                final = score / self.tries[name].size
                if final > highest:
                    temp = name
                    highest = final
                    score = 0
            prediction.append(temp)
            score = 0
            highest = -10
        return prediction
