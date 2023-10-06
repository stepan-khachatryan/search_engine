# build the search index

# dicionary where: 
# keys: Doc IDs
# value: Term (word) position
from collections import defaultdict
import xml.etree.ElementTree as ET
from searchindex.preprocessing import preprocess_text
import sys


class TermDocuments(defaultdict):
    def __init__(self):
        super().__init__(list)

    @property
    def doc_freq(self):
        return len(self)

class Index(defaultdict):
    def __init__(self):
        super().__init__(TermDocuments)

        self.doc_count = 0

def build_index():
    print("Building index...")

    index = Index()

    with open('searchindex/datasets/ai.xml', 'r', encoding='utf-8') as f:
        for _, elem in ET.iterparse(f):
            if elem.tag == "row":
                doc_id = elem.attrib["Id"]
                text = elem.attrib["Body"].strip()

                terms = preprocess_text(text)
                index.doc_count += 1

                for position, term in enumerate(terms):
                    index[term][doc_id].append(position)
    return index

def build_and_print():
    index = build_index()
    index_print = [""]
    index_print.append(f"doc_count: {index.doc_count}")
    for term in sorted(index):
        index_print.append(f"{term}: {index[term].doc_freq}")
        for doc in index[term]:
            index_print.append(f"\t{doc}: {','.join([str(x) for x in sorted(index[term][doc])])}")
    return '\n'.join(index_print)


index = []
if 'runserver' in sys.argv:
    index = build_index()