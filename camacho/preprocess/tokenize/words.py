from camacho.base import TransformerMixin
from nltk import word_tokenize


class WhitespaceTokenizer(TransformerMixin):
    """
    Tokenize text on whitespace.
    
    Useful for using the output of some other tokenization system.
    """

    def transform(self, texts):
        return map(lambda s: s.split(), texts)


class NLTKTokenizer(TransformerMixin):
    """
    Wraps NLTK's word_tokenize().
    """

    def transform(self, texts):
        return map(word_tokenize, texts)
