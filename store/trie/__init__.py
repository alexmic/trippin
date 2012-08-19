"""
Implementation of a Trie.
"""
from collections import defaultdict
from helpers import group_by_word_id
import sys

class Node(object):

    def __init__(self):
        self.children = defaultdict(Node)
        self.words = set()

    def __getitem__(self, key):
        return self.children[key]

    def flatten_words(self):
        words = []
        for w in self.words:
            words.append(w)
        for _, node in self.children.iteritems():
            words.extend(node.flatten_words())
        return words 

    def add_word(self, wid, index):
        """ Adds a word - does not actually store the word
            but it's index in the sentence for less memory.
        """
        if wid and index is not None and index >= 0:
            self.words.add((wid, index))

class Trie(object):

    def __init__(self):
        self.root = Node()
        self.count = 0

    def insert(self, wid, index, word, data=None):
        """ Inserts a word into the trie. Associates that
            word with the word id (wid) and its index in
            the sentence it was part of.
        """
        if wid and word and index is not None and index >= 0:
            node = self.root
            for ch in word:
                node = node[ch.lower()]
            node.add_word(wid, index)
            self.count += 1
        
    def delete(self, value):
        pass

    def query(self, words, match_all=True):
        """ Queries the trie and returns a list of hits. 
            words
                a list of words which make up the query
            match_all
                a flag that denotes whether we want *all* the
                query tokens to match in order for an entry
                to be considered a hit e.g 'red tree house' will
                be a hit only if we have a prefix for red and tree
                and house
        """
        words_length = len(words)
        candidate_results = []
        for word in words:
            node = self.root
            for ch in word:
                node = node[ch]
            candidate_results.extend(node.flatten_words())
        candidate_groups = group_by_word_id(candidate_results)
        is_hit = lambda w: not match_all or (match_all and len(w[1]) == words_length)
        return filter(is_hit, candidate_groups.iteritems())

    def status(self):
        num_nodes = 0
        stack = [self.root]
        while stack:
            top = stack.pop()
            num_nodes += 1
            for ch in top.children:
                stack.append(top.children[ch])
        return {
            "items": self.count, 
            "nodes": num_nodes
        }
        
        