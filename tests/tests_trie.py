from trippin.store.trie import Node
from trippin.store.trie import Trie
from trippin.store.trie.helpers import group_by_word_id

import unittest2

class TrieNodeTests(unittest2.TestCase):

    def test_add_word(self):
        node = Node()
        node.add_word(1, 0)
        node.add_word(None, 2)
        node.add_word(3, None)
        node.add_word(4, -1)
        self.assertTrue((1, 0) in node.words)
        self.assertFalse((None, 2) in node.words)
        self.assertFalse((3, None) in node.words)
        self.assertFalse((4, -1) in node.words)

    def test_add_children(self):
        node = Node()
        node.children['a'] = 1
        node.children['b'] = 2
        self.assertEqual(node['a'], 1)
        self.assertEqual(node['b'], 2)

    def test_flatten_words(self):
        node = Node()
        node.add_word(1, 0)
        node.add_word(2, 1)
        node['a'].add_word(3, 0)
        node['a'].add_word(4, 1)
        node['b'].add_word(5, 2)
        node['b']['c'].add_word(6, 0)
        words = node.flatten_words()
        expected = [(1, 0), (2, 1), (4, 1), (3, 0), (5, 2), (6, 0)]
        for e in expected:
            self.assertTrue(e in words)

class TrieTests(unittest2.TestCase):
    
    def test_insert(self):
        trie = Trie()
        trie.insert(1, 0, 'foo')
        trie.insert(2, 0, 'bar')
        trie.insert(3, 0, 'baz')
        trie.insert(None, 0, 'bar')
        trie.insert(4, -1, 'booz')
        trie.insert(5, None, 'baj')
        words = trie.root.flatten_words()
        expected = [(1, 0), (2, 0), (3, 0)]
        for e in expected:
            self.assertTrue(e in words)
        self.assertFalse((None, 0) in words)
        self.assertFalse((4, -1) in words)
        self.assertFalse((5, None) in words)

    def test_insert_keeps_correct_count(self):
        trie = Trie()
        trie.insert(1, 0, 'foo')
        trie.insert(2, 0, 'bar')
        trie.insert(3, 0, 'baz')
        trie.insert(None, 0, 'bar')
        trie.insert(4, 0, None)
        trie.insert(5, None, 'biz')
        self.assertEqual(trie.count, 3)

class TrieHelpersTests(unittest2.TestCase):

    def test_group_by_word_id(self):
        wordlist = [(1, 0), (2, 8), (1, 1), (3, 20),
                    (2, 10), (None, 11), (3, None), (3, -1)]
        groups = group_by_word_id(wordlist)
        self.assertTrue(0 in groups[1])
        self.assertTrue(1 in groups[1])
        self.assertTrue(8 not in groups[1])
        self.assertTrue(8 in groups[2])
        self.assertTrue(10 in groups[2])
        self.assertTrue(0 not in groups[2])
        self.assertTrue(20 in groups[3])
        self.assertTrue(11 not in groups[1])
        self.assertTrue(11 not in groups[2])
        self.assertTrue(11 not in groups[3])
        self.assertTrue(None not in groups[3])
        self.assertTrue(-1 not in groups[3])

if __name__ == "__main__":
    unittest2.main()