"""
Name:Che-Jui (Jerry), Chang
Coding Challenge 7 - Lonely Rolling Star - Solution Code
CSE 331 Fall 2020
Professor Sebnem Onsay
"""
from operator import itemgetter
from typing import List, Tuple


class Item:
    """
    A class that will store an item's name and category
    """
    def __init__(self, item_name: str, item_category: str):
        self.name = item_name
        self.category = item_category

    def __repr__(self):
        return "Item('" + self.name + "','" + self.category + "')"

    def get_name(self) -> str:
        """
        returns the strng representing the item's name
        :return: Item name string
        """
        return self.name

    def get_category(self) -> str:
        """
        Returns the string representation of the item's category
        :return: Item category string
        """
        return self.category


class RoboKingOfAllCosmos:

    def __init__(self):
        self.data = []
        # put your scoring container here

    def construct_score_book(self, items_and_size: List[Tuple[str, float]]) -> None:
        """
        create a score book to set self.data with list of tuple
        :param items_and_size: the stuff we are adding into self.data
        :return: None
        """
        for each in items_and_size:
            if each not in self.data:
                self.data.append(each)

    def get_score_book(self) -> List[Tuple[str, float]]:
        """
        get the score book, return it.
        :return: self.data
        """
        return self.data

    def judge_katamari(self, katamari_contents: List[Item]) -> Tuple[float, List[Tuple[str, int]], List[str]]:
        """
        first, create a dictionary contains the count of each different category.
        if it's cousins, we add the name into the cousin list.
        After create the dictionary, we need to get the top three score's category.
        We also need to calculate the score and check if the name matches
        the name in self.data, then sums up the score and round it.
        :param katamari_contents: the information we using to create the dictionary
        :return: the score, top 3 scored category, cousin_list
        """
        score = 0
        katamari = {}
        cousin_list = []
        for each in katamari_contents:
            if each.category not in katamari:
                katamari[each.category] = 1
            else:
                katamari[each.category] += 1
            if each.category == 'cousins':
                cousin_list.append(each.name)
        for items in self.data:
            for check in katamari_contents:
                if items[0] == check.name:
                    score += items[1]
        katamari = sorted(katamari.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        print(katamari)
        katamari = katamari[:3]
        return round(score, 1), katamari, cousin_list
