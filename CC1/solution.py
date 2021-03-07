"""
Che-Jui (Jerry), Chang
Coding Challenge 1 - Sort of Sorted - Solution Code
CSE 331 Fall 2020
Professor Sebnem Onsay
"""
from typing import List


def sort_of_sorted(data: List[str]) -> (int, List[str]):
    """
    Determine the longest sublist of strings in alphabetical order.
    :param data: [list] of strings in semi-sorted order

        [0]: [int] length of longest sorted sublist
        [1]: [list] longest sorted sublist of strings
    """
    match = []
    temp = []
    size = 0
    compare = "'"
    answer = []
    count = 0
    for word in data:
        if word >= compare:
            match.append(word)
        else:
            temp.append(match[:])
            match.clear()
            match.append(word)
            if word == data[-1]:
                temp.append(match)
        compare = word
    if len(match) > 1:
        temp.append(match)
    for i in range(len(temp)):
        if len(temp[i]) > size:
            start = 0
            count = 0
            hold = temp[i]
            temp[i] = temp[0]
            temp[0] = hold
            size = len(temp[0])
            start += 1
            count += 1
        elif len(temp[i]) == size:
            hold = temp[i]
            temp[i] = temp[start]
            temp[start] = hold
            start += 1
            count += 1
        else:
            continue
    if count == 0:
        zero = [0, []]
        zero = tuple(zero)
        return zero
    answer.append(len(temp[0]))
    answer.append(temp[0])
    answer = tuple(answer)
    return answer
