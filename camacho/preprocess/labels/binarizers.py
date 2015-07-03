from camacho.base import ReversibleTransformerMixin
import numpy as np


def to_one_hot(n, count):
    nn = [0] * count
    nn[n] = 1
    return nn


def dict_from_list(aa):
    aa = sorted(set(aa))
    nn = range(len(aa))
    a2n = dict(zip(aa, nn))
    n2a = dict(zip(nn, aa))
    return a2n, n2a


def dict_from_lists(aaa):
    rr = set()
    for aa in aaa:
        for a in aa:
            rr.add(a)
    return dict_from_list(rr)


class LabelBinarizer(ReversibleTransformerMixin):
    """
    Labels <-> one-hot arrays.
    """

    def fit(self, aa):
        self._a2n, self._n2a = dict_from_list(aa)
        return self

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
        self._a2n, self._n2a = dict_from_lists(aaa)
        return self

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


class OneHotListBinarizer(ReversibleTransformerMixin):
    """
    Lists of tokens <-> concatenated one-hot arrays per token.
    """

    def fit(self, aaa):
        self._a2n, self._n2a = dict_from_lists(aaa)
        return self

    def transform(self, aaa):
        rrr = []
        count = len(self._a2n)
        for aa in aaa:
            nn = map(lambda a: self._a2n[a], aa)
            nnn = map(lambda n: to_one_hot(n, count), nn)
            nn = reduce(lambda a, b: a + b, nnn)
            rrr.append(nn)
        return rrr
