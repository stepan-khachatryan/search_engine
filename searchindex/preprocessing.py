# Preprocess text for searching
import re
from nltk.stem import SnowballStemmer

with open("searchindex/datasets/stopwords_en.txt") as f:
    enStopWords = set(f.read().splitlines())

stemmer = SnowballStemmer('english')

def preprocess_text(text: str) -> list[str]:

    tokens = text.lower()

    tokens = re.split(r"[^\w]", tokens)

    tokens = [stemmer.stem(x) for x in tokens if x and x not in enStopWords]

    return tokens