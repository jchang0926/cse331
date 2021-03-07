"""
Name:Che-Jui (Jerry), Chang
Project 2 - Hybrid Sorting - Starter Code
CSE 331 Fall 2020
Professor Sebnem Onsay
"""
from typing import List, Any, Dict


def hybrid_sort(data: List[Any], threshold: int) -> None:
    """Use merge_sort first with threshold, if the len of data is bigger than
    threshold, then we use insertion sort"""
    merge_sort(data, threshold)


def inversions_count(data: List[Any]) -> int:
    """Use merge_sort to find the inversion count when there's a number that's bigger
    than any number after it, we plus 1"""
    return merge_sort(data)


def merge_sort(data: List[Any], threshold: int = 0) -> int:
    """Start with a list of data, we check the len(data) if it's bigger than threshold,
    if it is, then use insertion sort. otherwise, use merge sort and get the inversion count.
    we only return the inversion count, we sort the list in space."""
    count = len(data)
    if count < threshold:
        insertion_sort(data)
    if count > 1:
        mid = count // 2
        list1 = data[:mid]
        list2 = data[mid:]
        l1_inv = merge_sort(list1, threshold)
        l2_inv = merge_sort(list2, threshold)
        inv = l1_inv + l2_inv
    else:
        return 0
    i = j = 0
    while i+j < len(data):
        if j == len(list2) or (i < len(list1) and list1[i] <= list2[j]):
            data[i+j] = list1[i]
            i += 1
        else:
            data[i+j] = list2[j]
            j += 1
            inv += len(list1)-i
    if threshold != 0:
        return 0
    return inv


def insertion_sort(data: List[Any]) -> None:
    """goes from the start of the list, takes the value in index 1 and compare it to
    the previous one. If the value is bigger than previous, keep going until it's the
    start of the list. Otherwise, keep checking until the end of the list or find a
    value that's smaller than the value and insert it after finding the smallest one."""
    count = len(data)
    if count == 0:
        return data
    for i in range(1, count):
        key = data[i]
        j = i-1
        while j >= 0 and key < data[j]:
            data[j+1] = data[j]
            j -= 1
        data[j+1] = key


def find_match(user_interests: List[str], candidate_interests: Dict[str, List]) -> str:
    """we create a dictionary with user_interests where key is the hobby and value is the score.
    Then we go through candidate_interests list then compare the hobby in the user_interests and
    add the score to temp. Then compare the score to find out the lowest score and return the name
    with the lowest inversion count compare to user."""
    score_dict = {}
    scores = 0
    less = 100
    for item in user_interests:
        score_dict[item] = scores
        scores += 1
    for name, order in candidate_interests.items():
        temp = []
        for hobby in order:
            temp.append(score_dict[hobby])
        count = inversions_count(temp)
        if count < less:
            match = name
            less = count
    return match





