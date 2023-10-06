from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

def summarise(document):

    # Initialize the Luhn Summarizer
    summarizer = LuhnSummarizer()

    # Parse the document into words
    parser = PlaintextParser(document, Tokenizer('english'))

    # Generate the summary. sentences_count controls the number of sentences
    summary = summarizer(parser.document, sentences_count=2)

    # Join the sentences together separated by a space
    summary = ' '.join([str(s) for s in summary])

    return summary