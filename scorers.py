"""
Various scoring functions. Each scoring function takes the matched
sentence, a list of query tokens and a list of indexes which represent 
the words that were matched by the indexing engine.
"""

def match_length(sentence_tokens, query_tokens, indexes):
    score = 0
    for i in indexes:
        fw = sentence_tokens[i]
        for qt in query_tokens:
            if qt in fw:
                diff = len(fw) - len(qt)
                score += 1.0 / (diff + 1)
    return score