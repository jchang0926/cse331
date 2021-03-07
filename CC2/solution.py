"""
Che-Jui (Jerry), Chang
Coding Challenge 2 - Drop It Like It's Hot - Unit Tests
CSE 331 Fall 2020
Professor Sebnem Onsay
"""
from typing import List, Tuple


def firefighter(grid: List[List[int]], k: int) -> Tuple[int, int, int]:
    """
    Given an n x n 2D list of 0's and 1's and an integer k, determine the greatest number of 1's
    that can be covered by a square of size k x k. Return a tuple (a, b, c) where
        a = number of 1's this optimal k x k square covers
        b = the row of the top left corner of this square
        c = the col of the top left corner of this square
    :param grid: [list[list[int]]] a square 2D list of 0, 1 integers
    :param k: [int] the size of the square placed to cover 1's
    :return: [tuple[int, int, int]] a tuple (a, b, c) where
        a = number of 1's this optimal k x k square covers
        b = the row of the top left corner of this square
        c = the col of the top left corner of this square
    """
    highest = 0
    top_left_row = 0
    top_left_col = 0

    if len(grid) == 1:
        return 0, 0, 0

    for row in range(len(grid)-k+1):
        for col in range(len(grid)-k+1):
            sum_of_squares = 0
            count = 0
            next_row = 0
            next_col = 0
            while count < k*k:
                sum_of_squares += grid[row + next_row][col + next_col]
                if next_col < k-1:
                    next_col += 1
                elif next_row < k-1:
                    next_row += 1
                    next_col = 0
                count += 1
            if sum_of_squares > highest:
                highest = sum_of_squares
                top_left_row = row
                top_left_col = col
    answer = [highest, top_left_row, top_left_col]
    answer = tuple(answer)
    return answer
