from camacho.base import TransformerMixin
import unicodedata


class CodeUnitTokenizer(TransformerMixin):
    """
    Tokenize text on code units (which are often user-perceived characters).

    Unicode combining characters are treated as separate entities, which may not
    be what you want.  This is faster than combining them (see
    CharacterTokenizer).
    """

    def transform(self, texts):
        return map(list, texts)


def segments_from_text(text):
    """
    text -> list of str

    Does not group jamo.
    """
    nn = map(unicodedata.combining, text)
    buf = []
    rr = []
    for c, n in zip(text, nn):
        if n:
            buf.append(c)
            continue
        if buf:
            rr.append(buf)
        buf = [c]
    if buf:
        rr.append(buf)
    return map(lambda r: ''.join(r), rr)


class CharacterTokenizer(TransformerMixin):
    """
    Tokenize text on user-perceived character boundaries.
    
    You will almost certainly want to do Unicode normalization beforehand!
    Slower than CodeUnitTokenizer.
    """

    def transform(self, texts):
        return map(segments_from_text, texts)


class WhitespaceTokenizer(TransformerMixin):
    """
    Tokenize text on whitespace (eg, for using the output of some other
    tokenization system).
    """

    def transform(self, texts):
        assert self._fitted
        return map(lambda s: s.split(), texts)
