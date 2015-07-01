from camacho.base import ReversibleTransformerMixin
from camacho.base import k2v_from_v2k
import numpy as np


def to_one_hot(n, count):
    nn = [0] * count
    nn[n] = 1
    return nn


class LabelBinarizer(ReversibleTransformerMixin):
    """
    Labels <-> one-hot arrays.
    """

    def fit(self, aa):
        aa = sorted(set(aa))
        self._a2n = dict(zip(aa, xrange(len(aa))))
        self._n2a = k2v_from_v2k(self._a2n)

    def transform(self, aa):
        nn = map(lambda a: self._a2n[a], aa)
        return map(lambda n: to_one_hot(n, len(self._a2n)), nn)

    def inverse_transform(self, nnn):
        nn = map(np.argmax, nnn)
        return map(lambda n: self._n2a[n], nn)


def ones_and_zeros(one_indexes, count):
    nn = [0] * count
    for x in one_indexes:
        nn[x] = 1
    return nn


class SetBinarizer(ReversibleTransformerMixin):
    """
    Lists of labels <-> bitsets.
    """

    def fit(self, aaa):
        aa_set = set()
        for aa in aaa:
            for a in aa:
                aa_set.add(a)
        aa = sorted(aa_set)
        self._a2n = dict(zip(aa, xrange(len(aa))))
        self._n2a = k2v_from_v2k(self._a2n)

    def transform(self, aaa):
        nnn = []
        count = len(self._a2n)
        for aa in aaa:
            nn = map(lambda a: self._a2n[a], set(aa))
            nn = ones_and_zeros(nn, count)
            nnn.append(nn)
        return nnn

    def inverse_transform(self, nnn):
        aaa = []
        for nn in nnn:
            aa = map(lambda n: self._n2a[n], nn)
            aaa.append(aa)
        return aaa
