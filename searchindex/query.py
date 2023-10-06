from cgitb import text
from collections import defaultdict
import math
from posixpath import split
from turtle import position
from searchindex.build_index import index
from searchindex.preprocessing import preprocess_text
import re
from collections import defaultdict
import math
from math import log10
from searchengine.models import Document
def run_query(query):

    if " AND NOT " in query:
        word1, word2 = query.split("AND NOT")
        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]
        results1 = index[word1]
        results2 = index[word2]
        results = [i for i in results1 if i not in results2]
        return results
    elif " OR NOT " in query:
        word1, word2 = query.split("OR NOT")
        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]
        results1 = set(index[word1])
        results2 = index[word2]

        not_results2 = set()
        for i in Document.objects.values_list('doc_id')[:100]:
            i = str(i[0])
            if i not in results2:
                not_results2.add(i)

        return list(results1.union(not_results2))
    elif " OR " in query:
        word1, word2 = query.split("OR")
        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]
        results1 = set(index[word1])
        results2 = set(index[word2])
        return list(results1.union(results2))
    elif " AND " in query:
        word1, word2 = query.split("AND")
        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]
        results1 = index[word1]
        results2 = index[word2]
        results = [r for r in results1 if r in results2]
        return results

    elif query.startswith('"') and query.endswith('"'):
        word1, word2 = query.split(" ")
        word1 = preprocess_text(word1)[0]
        word2 = preprocess_text(word2)[0]
        results1 = index[word1]
        results2 = index[word2]
        print(results1)
        print(results2)
        result_ids = set()
        for i in results1:
            pos1 = index[word1][i]
            pos2 = index[word2][i]
            results = [j for j in pos1 if j + 1 in pos2]
            if results:
                result_ids.add(i)
        print(result_ids)
        return result_ids
    elif query.startswith('#') and query.endswith(')'):
        num = int(query[1: query.find("(")])
        tokens = query[(query.find("(") + 1): -1]
        word1, word2 = preprocess_text(tokens)
        results1 = index[word1]
        results2 = index[word2]

        result_ids = set()
        for i in results1:
            pos1 = index[word1][i]
            pos2 = index[word2][i]
            term_results1 = [j for j in pos1 if j + num in pos2]
            term_results2 = [j for j in pos1 if j - num in pos2]
            if term_results1 or term_results2:
                result_ids.add(i)

        return list(result_ids)

    results = run_ranked_search(query)
    return results

def run_ranked_search(query):
    results = defaultdict(float)

    query = preprocess_text(query)

    for term in query:
        docs = index[term]
        for doc_id in docs:
            tf = len(docs[doc_id])
            df = docs.doc_freq

            w  = (1 + math.log10(tf)) * math.log10(index.doc_count / df)

            results[doc_id] += w
    return sorted(results, key=results.get, reverse=True)