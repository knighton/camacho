from camacho.base import Transformer
from nltk import word_tokenize


class WhitespaceTokenizer(Transformer):
    """
    Tokenize text on whitespace.
    
    Useful for using the output of some other tokenization system.
    """

    def transform(self, texts):
        return map(lambda s: s.split(), texts)


class NLTKTokenizer(Transformer):
    """
    Wraps NLTK's word_tokenize().
    """

    def transform(self, texts):
        return map(word_tokenize, texts)
