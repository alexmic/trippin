"""
The store abstracts the underlying indexing mechanism, which
can be changed by setting INDEXING_ENGINE in your settings.

A store expects an indexing engine to implement the following methods:

 - status(): The indexing engine should return what it deems useful.
 
 - insert(wid, index, word): The store will brake the sentence on white space and
    then call insert() for all the words, passing a unique word id, the index
    of the word in the sentence and the word to be inserted. 
 
 - delete(): Not implemented yet.

 - query(): The store will call query() on the index passing a list of tokens
    to be searched for. It then expects as a response a list of hits. A hit
    is a tuple of (wid, [indexes], where 'wid' is the word id and 'index'
    are the indexes of the matched words in their parent sentence.
"""
import uuid

class Store(object):

    def __init__(self, index, scorer):
        self.index = index
        self.scorer = scorer
        self.sentence_map = {}
        self.data_map = {}

    def status(self):
        return self.index.status()

    def insert(self, sentence, data=None):
        """ Inserts a sentence into the store. Assigns a unique word id 
            to the sentence so we can retrieve it (and any stored data) 
            in full after the results are calculated. It also passes the
            index of each word in the sentence so we can use it afterwards
            when scoring.
        """ 
        if not sentence: return
        wid = uuid.uuid4().hex
        for index, word in enumerate(sentence.split()):
            self.index.insert(wid, index, word.lower().strip())
        if data is not None:
            self.data_map[wid] = data
        self.sentence_map[wid] = sentence
        return wid

    def delete(self):
        pass
    
    def query(self, query, include_data=True):
        """ Queries the index and returns a list of hits 
            scored accordingly. 
        """
        query_tokens = map(lambda q: q.lower().strip(), query.split())
        hits = self.index.query(query_tokens)
        results = []
        for wid, indexes in hits:
            sentence = self.sentence_map[wid]
            sentence_tokens = map(lambda s: s.lower().strip(), sentence.split())
            score = self.scorer(sentence_tokens, query_tokens, indexes)
            results.append((score, sentence))
        return results