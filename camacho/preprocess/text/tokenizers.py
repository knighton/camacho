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


def segment_raw(text):
    """
    Don't do any normalization before segmenting text.

    * Useful when you have already done some form of Unicode normalization
      before you want to segment into characters as-is.

    * Otherwise, a bad choice.

    * Does not group jamo.
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


def segment_nfc(text):
    """
    Applies NFC normalization, then segments.

    * Useful if you (a) haven't already normalized, and (b) don't trust
      segment_aggressive().

    * Does not group jamo.
    """
    text = unicodedata.normalize('nfc', text)
    return segment_raw(text)


def reorder_segment(nn_cc):
    nn_cc.sort()
    return ''.join(map n, c: c, nn_cc)


def segment_aggressive(text):
    """
    Aggressively normalizes text before segmentation.

    * Combining characters can interact in a way that inhibits combining,
      depending on how they are ordered.  So we enforce a canonical order before
      normalization.

    * Does not group jamo.
    """
    # Decompose.
    text = unicodedata.normalize('nfd', text)

    # Segment.
    nn = map(unicodedata.combining, text)
    buf = []
    nnn_ccc = []
    for c, n in zip(text, nn):
        if n:
            buf.append((n, c))
            continue
        if buf:
            nnn_ccc.append(buf)
        buf = [(n, c)]
    if buf:
        nnn_ccc.append(buf)

    # Reorder decomposed segments in a non-standards-compliant way.
    ss = map(reorder_segment, nnn_ccc)

    # Now, NFC-normalize that.
    return map(lambda s: unicodedata.normalize('nfc', s), ss)


class CharacterTokenizer(TransformerMixin):
    """
    'Tokenize' text on user-perceived characters.
    
    Joins Unicode combining characters.  Slower than CodeUnitTokenizer.
    """

    def __init__(self, norm='aggressive'):
        self._norm = norm
        self._segment_f = {
            'raw': segment_raw,
            'nfc': segment_nfc,
            'aggressive': segment_aggressive,
        }[norm]
        self._fitted = False

    def fit(self, texts):
        self._fitted = True
        return self

    def fit_transform(self, texts):
        self.fit()
        return self.transform()

    def transform(self, texts):
        assert self._fitted
        return map(self._segment_f, texts)


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
