"""
Name:Che-Jui (Jerry), Chang
CC3 - Starter Code
CSE 331 Fall 2020
Professor Sebnem Onsay
"""
# import math
from typing import List


def find_missing_value(sequence: List[int]) -> int:
    """the big function is some base case of this function
    when the start is not 0 or when the list is empty"""

    def find_missing_value_recursive(start: int, end: int) -> int:
        """use quick sort to find the missing number by slicing the part
        that contain less number and call the function recursively."""
        mid = (start + end) // 2

        if start == mid:
            return mid + 1
        elif mid == sequence[mid]:
            return find_missing_value_recursive(mid, end)
        else:
            return find_missing_value_recursive(start, mid)

    count = len(sequence)
    if count == 0:
        return 0
    if sequence[0] != 0:
        return 0
    return find_missing_value_recursive(0, count)
