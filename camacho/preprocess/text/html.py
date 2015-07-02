from camacho.base import TransformerMixin
from HTMLParser import HTMLParser


class HTMLEntityDecoder(TransformerMixin):
    """
    Decode the HTML entities in text.
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
