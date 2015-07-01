from camacho.base import TransformerMixin
from camacho.util import v2k_from_k2v
from collections import defaultdict


def assign_ints_by_freq(a2count):
    count2aa = defaultdict(list)
    for a, count in a2count.iteritems():
        count2aa[count].append(a)

    a2n = {}
    for count in sorted(count2aa, reversed=True):
        for a in sorted(count2aa[count]):
            n = len(a2n) + 1
            a2n[a] = n

    return a2n


class StandardEncoder(TransformerMixin):
    def __init__(self, min_freq=50, oov_int=0, oov_token=' '):
        self._min_freq = min_freq
        self._oov_int = oov_int
        self._oov_token = oov_token

    def fit(self, aaa):
        # Count tokens.
        a2count = defaultdict(int)
        for aa in aaa:
            for a in aa:
                a2count[a] += 1

        # Drop the ones that are too infrequent.
        if self._min_freq is not None:
            for a, count in a2count.items():
                if count < self._min_freq:
                    del a2count[a]

        # Number the unique tokens by their frequency of occurence.  Save zero
        # for out-of-vocabulary tokens.
        self._a2n = assign_ints_by_freq(a2count)

        return self

    def fit_transform(self, aaa):
        self.fit(aaa)
        return self.transform(aaa)

    def transform(self, aaa):
        nnn = []
        for aa in aaa:
            nn = map(lambda a: self._a2n.get(a, self._oov_int), aa)
            nnn.append(nn)
        return nnn
