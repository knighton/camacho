from camacho.base import TransformerMixin
import unicodedata


class CodeUnitTokenizer(TransformerMixin):
    """
    'Tokenize' text on code units (often user-perceived characters).

    Unicode combining characters are treated as separate entities, which may not
    be what you want.  This is faster than combining them (see
    CharacterTokenizer).

    On wide python builds, code unit == code point.  On narrow python builds,
    beware surrogate pairs.
    """

    def __init__(self):
        self._fitted = False

    def fit(self, texts):
        self._fitted = True
        return self

    def fit_transform(self, texts):
        self._fitted = True
        return map(list, texts)

    def transform(self, texts):
        assert self._fitted
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
    'Tokenize' text on user-perceived characters.
    
    Joins Unicode combining characters.  Slower than CodeUnitTokenizer.
    """

    def __init__(self):
        self._fitted = False

    def fit(self, texts):
        self._fitted = True
        return self

    def fit_transform(self, texts):
        self.fit()
        return self.transform()

    def transform(self, texts):
        assert self._fitted
        return map(segments_from_text, texts)


class WhitespaceTokenizer(TransformerMixin):
    """
    Tokenize text on whitespace (eg, for using some other system's tokenization
    results).
    """

    def __init__(self):
        self._fitted = False

    def fit(self, texts):
        self._fitted = True
        return self

    def fit_transform(self, texts):
        self._fitted = True
        return map(lambda s: s.split(), texts)

    def transform(self, texts):
        assert self._fitted
        return map(lambda s: s.split(), texts)
