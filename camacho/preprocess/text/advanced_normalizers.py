from camacho.base import TransformerMixin
import unicodedata


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


class IntraUPCReorderer(TransformerMixin):
    """
    Normalize a bit further than the standard Unicode normalization forms.

    Decomposes, reorders segments, then recomposes.  Drop-in replacement for
    UnicodeNormalizer.

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


class ExtraNFKD(TransformerMixin):
    def __init__(self):
        d = {}
        self._replacer = CharacterReplacer(d)

    def transform(self, texts):
        return self._replacer.transform(texts)
