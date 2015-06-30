from camacho.base import TransformerMixin


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


def segment_upc(text):
    buf = []
    for c in text:
        n = unicodedata.combining(c)
        if n:
            buf.append(c)
            continue
        if buf:
            yield ''.join(buf)
        buf = [c]
    if buf:
        yield ''.join(buf)


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
        self._fitted = True
        return map(segment_upc, texts)

    def transform(self, texts):
        assert self._fitted
        return map(segment_upc, texts)


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
