#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:10:20 2024

@author: claremalhotra
"""


def make_change(total):
    """
    This function returns the distinct combinations of coins that
    add to a given total
    """
    coin_vals = [100, 25, 10, 5, 1]
    coin_options = []
    coin_vals2 = [x for x in coin_vals if total >= x]
    if len(coin_vals2) == 0:
        return [[]]
    for i in coin_vals2:
        inner_results = make_change(total-i)
        for result in inner_results:
            coin_options.append([i] + result)
    unique_coins = []
    for coin_option in coin_options:
        coin_option.sort()
        if coin_option not in unique_coins:
            unique_coins.append(coin_option)
    return unique_coins


def dict_filter(func, dic):
    """This function produces a dictionary where a given key and value
    remain associated with each other in the new dictionary, if
    and only if the function returns True when called with
    the key and the value.
    """
    dic2 = {}
    for k, v in dic.items():
        if func(k, v):
            dic2[k] = v
    return dic2


class KVTree:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def treemap(fn, tree):
    """This function takes in a function and a tree and modifies the tree
    according to the function"""
    # if len(self.children) == 0:
    #     self.children = fn(tree)
    #     return
    tree.key, tree.value = fn(tree.key, tree.value)
    for child in tree.children:
        return treemap(fn, child)


def print_tree(tree):
    print(tree.key)
    print(tree.value)
    for child in tree.children:
        return print_tree(child)


class DTree:
    def __init__(self, variable, threshold, lessequal, greater, outcome):
        self.variable = variable
        self.threshold = threshold
        self.lessequal = lessequal
        self.greater = greater
        self.outcome = outcome
        if (self.variable is not None and self.threshold is not None
            and self.lessequal is not None and self.greater is not None) \
            and (self.outcome is not None):
            raise ValueError
        if (self.variable is not None and self.threshold is not None
            and self.lessequal is not None and self.greater is not None) \
            or (self.outcome is not None):
            return
        else:
            raise ValueError

    def tuple_atleast(self):
        def tuple_helper(node):
            index = node.variable

            if node.outcome is not None:
                return index

            lessequal_index = tuple_helper(node.lessequal) if node.lessequal \
                else float('-inf')
            if lessequal_index is not None and lessequal_index > index:
                index = lessequal_index

            greater_index = tuple_helper(node.greater) if node.greater else \
                float('-inf')
            if greater_index is not None and greater_index > index:
                index = greater_index
            return index
        max_index = tuple_helper(self)
        if self.outcome is None:
            return max_index + 1
        else:
            return max_index

    def find_outcome(self, observations):
        if self.outcome is not None:
            return self.outcome
        if observations[self.variable] <= self.threshold:
            inner_tree = self.lessequal.find_outcome(observations)
            return inner_tree
        inner_tree = self.greater.find_outcome(observations)
        return inner_tree

    def no_repeats(self):
        # helper function will take the list of things you've seen and
        # see if any of the children check it
        seen = []

        def children_check(node, seen):
            if node.outcome is not None:
                return True
            if node.variable in seen:
                return False
            seen.append(node.variable)
            if not children_check(node.lessequal, seen):
                return False
            if not children_check(node.greater, seen):
                return False
            return True
        return children_check(self, seen)
