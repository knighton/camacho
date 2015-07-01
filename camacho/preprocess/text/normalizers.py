from camacho.base import TransformerMixin
import unicodedata


class LowerCaseNormalizer(TransformerMixin):
    """
    Convert to lower case.
    """

    def transform(self, texts):
        return map(lambda s: s.lower, texts)


class UnicodeNormalizer(TransformerMixin):
    """
    Apply one of the Unicode normalization forms.
    """

    def __init__(self, form='NFC'):
        assert form in ('NFC', 'NFD', 'NFKC', 'NFKD')
        self._form = form

    def transform(self, texts):
        return map(lambda s: unicodedata.normalize(self._form, s), texts)


def aggressively_normalize(text):
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


class AggressiveUnicodeNormalizer(TransformerMixin):
    """
    Normalize a bit further than the standard Unicode normalization forms.

    Decomposes, reorders segments, then recomposes.  Drop-in replacement for
    UnicodeNormalizer.
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
            text = aggressively_normalize(text)
            if self._after:
                text = unicodedata.normalize(self._after, text)
            rr.append(text)
        return rr


class WhitespaceNormalizer(TransformerMixin):
    """
    Replace all whitespace with ' '.
    """

    def transform(self, texts):
        return map(lambda s: u' '.join(s.split()), texts)
