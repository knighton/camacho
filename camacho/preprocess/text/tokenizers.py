from camacho.base import TransformerMixin


class CodeUnitTokenizer(TransformerMixin):
    """
    'Tokenize' text on a per-character basis.

    Naively treat each code unit as a character.  Fast and probably good enough
    in practice.  For the technically correct way to do this, see
    GraphemeClusterTokenizer.

    On wide python builds, code unit == code point.  On narrow python builds,
    beware surrogate pairs.
    """

    name = 'code_unit_tokenizer'

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


class GraphemeClusterTokenizer(TransformerMixin):
    """
    Tokenize text on a per-character basis.
    
    Accounts for Unicode combining characters.  Slower than CodeUnitTokenizer.
    """

    name = 'grapheme_cluster_tokenizer'

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

    name = 'whitespace_tokenizer'

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
