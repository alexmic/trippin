"""
Helper methods for the trie store.
"""
from collections import defaultdict

def group_by_word_id(word_list):
    """ Groups word (index) hits on word id. """
    histogram = defaultdict(list)
    for wid, index in word_list:
        if wid and index is not None and index >= 0:
            histogram[wid].append(index)
    return histogram