from camacho.preprocess.sequence import SequenceDestutterer
from camacho.preprocess.tokenize.characters import CharacterTokenizer


class TextDestutterer(Transformer):
    """
    Drop overly-repeated non-digit characters.
    """

    def __init__(self, max_consec=3):
        ignore = []
        for c in map(unichr, xrange(sys.maxunicode)):
            cat = unicodedata.category(c)
            if cat.startswith('N'):
                ignore.append(c)
        self._des = SequenceDestutterer(max_consec=max_consec, ignore=ignore)
        self._tok = CharacterTokenizer()

    def transform(self, texts):
        ccc = self._tok.transform(texts)
        ccc = self._des.transform(ccc)
        return map(lambda cc: ''.join(cc), ccc)
