from camacho.base import Transformer
import unicodedata


class UnicodeNormalizer(Transformer):
    """
    Apply one of the Unicode normalization forms.
    """

    def __init__(self, form='NFC'):
        assert form in ('NFC', 'NFD', 'NFKC', 'NFKD')
        self._form = form

    def transform(self, texts):
        return map(lambda s: unicodedata.normalize(self._form, s), texts)


def aggressively_normalize_upcs(text):
    nn = map(unicodedata.combining, text)

    tmp = []
    nnn_ccc = []
    for c, n in zip(text, nn):
        if n:
            tmp.append((n, c))
            continue
        if tmp:
            nnn_ccc.append(tmp)
        tmp = [(n, c)]
    if tmp:
        nnn_ccc.append(tmp)

    ss = []
    for nn_cc in nnn_ccc:
        nn_cc.sort()
        s = ''.join(map(lambda n, c: c, nn_cc))
        ss.append(s)

    return ''.join(ss)


class GraphemeClusterOrderer(Transformer):
    """
    Normalize a bit further than the standard Unicode normalization forms.

    Decomposes, reorders code units, then optionally recomposes.  Drop-in
    replacement for UnicodeNormalizer.

    If no 'before', assumes data is already decomposed.  The 'after' step is not
    required.
    """

    def __init__(self, before='NFD', after='NFC'):
        assert before in (None, 'NFD', 'NFKD')
        self._before = before

        assert after in (None, 'NFC', 'NFD', 'NFKC', 'NFKD')
        self._after = after

    def transform(self, texts):
        rr = []
        for text in texts:
            if self._before:
                text = unicodedata.normalize(self._before, text)
            text = aggressively_normalize_upcs(text)
            if self._after:
                text = unicodedata.normalize(self._after, text)
            rr.append(text)
        return rr
