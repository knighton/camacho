from camacho.base import TransformerMixin
from HTMLParser import HTMLParser
import unicodedata


class LowerCaser(TransformerMixin):
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


class WhitespaceNormalizer(TransformerMixin):
    """
    Replace all whitespace with ' '.
    """

    def transform(self, texts):
        return map(lambda s: u' '.join(s.split()), texts)


class CharacterReplacer(TransformerMixin):
    """
    Replace characters (single code units) with strings.
    """

    def __init__(self, s2s=None):
        if s2s is None:
            s2s = {}
        self._s2s = s2s
        for k, v in self._s2s.iteritems():
            assert isinstance(k, (str, unicode))
            assert len(k) == 1
            assert isinstance(v, (str, unicode))

    def transform(self, texts):
        rr = []
        for text in texts:
            cc = list(text)
            for i, c in enumerate(cc):
                v = self._s2s.get(c, None)
                if v is not None:
                    cc[i] = v
            rr.append(''.join(cc))
        return rr


class HTMLEntityDecoder(TransformerMixin):
    """
    Replace HTML entities in text.
    """

    def __init__(self, max_tries=10):
        assert isinstance(max_tries, int)
        assert 1 <= max_tries
        self._max_tries = max_tries

        self._parser = HTMLParser()

    def transform(self, texts):
        rr = []
        for text in texts:
            for i in range(self._max_tries):
                prev_text = text
                text = self._parser.unescape(text)
                if text == prev_text:
                    break
            rr.append(text)
        return rr
