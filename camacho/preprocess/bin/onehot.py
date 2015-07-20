from camacho.base import ReversibleTransformerMixin
from camacho.util import to_one_hot, ones_and_zeros, from_one_hot


def dict_from_list(aa):
    aa = sorted(set(aa))
    nn = range(len(aa))
    a2n = dict(zip(aa, nn))
    n2a = dict(zip(nn, aa))
    return a2n, n2a


class AtomBinarizer(ReversibleTransformerMixin):
    """
    Atoms <-> one-hot arrays.

    Used for binarizing labels.
    """

    def fit(self, aa):
        self._a2n, self._n2a = dict_from_list(aa)
        return self

    def transform(self, aa):
        nn = map(lambda a: self._a2n[a], aa)
        return map(lambda n: to_one_hot(n, len(self._a2n)), nn)

    def inverse_transform(self, nnn):
        nn = map(from_one_hot, nnn)
        return map(lambda n: self._n2a[n], nn)


def mapping_from_list(aa):
    aa = sorted(set(aa))
    nn = range(len(aa))
    a2n = dict(zip(aa, nn))
    n2a = dict(zip(nn, aa))
    return a2n, n2a


def mapping_from_lists(aaa):
    rr = set()
    for aa in aaa:
        rr.update(aa)
    return mapping_from_list(rr)


class SetBinarizer(ReversibleTransformerMixin):
    """
    Lists of unique tokens <-> Binary-encoded sets.

    Used for binarizing sets of labels.
    """

    def fit(self, aaa):
        for aa in aaa:
            assert len(set(aa)) == len(aa)
        self._a2n, self._n2a = mapping_from_lists(aaa)
        return self

    def transform(self, aaa):
        bbb = []
        count = len(self._a2n)
        for aa in aaa:
            nn = map(lambda a: self._a2n[a], aa)
            bb = ones_and_zeros(nn, count)
            bbb.append(bb)
        return bbb

    def inverse_transform(self, bbb):
        aaa = []
        for bb in bbb:
            nn = []
            for n, b in enumerate(bb):
                if b:
                    nn.append(n)
            aa = map(lambda n: self._n2a[n], nn)
            aaa.append(aa)
        return aaa


class OneHot1D(ReversibleTransformerMixin):
    """
    Token lists <-> concatenated one-hot arrays per token.

    Used for binarizing sequences.
    """

    def fit(self, aaa):
        self._a2n, self._n2a = mapping_from_lists(aaa)
        return self

    def transform(self, aaa):
        bbb = []
        count = len(self._a2n)
        for aa in aaa:
            nn = map(lambda a: self._a2n[a], aa)
            tmp_bbb = map(lambda n: to_one_hot(n, count), nn)
            bb = reduce(lambda a, b: a + b, tmp_bbb)
            bbb.append(bb)
        return bbb

    def inverse_transform(bbb):
        aaa = []
        count = len(self._a2n)
        for bb in bbb:
            nn = []
            assert not len(bb) % count
            for i in range(0, len(bb), count):
                sub_bb = bb[i : i + count]
                n = from_one_hot(sub_bb)
                nn.append(n)
            aa = map(lambda n: self._n2a[n], nn)
            aaa.append(aa)
        return aaa


class OneHot2D(ReversibleTransformerMixin):
    """
    Token lists <-> 2-dimensional one-hot arrays.

    Used for binarizing sequences.
    """

    def fit(self, aaa):
        self._a2n, self._n2a = mapping_from_lists(aaa)
        return self

    def transform(self, aaa):
        bbbb = []
        count = len(self._a2n)
        for aa in aaa:
            nn = map(lambda a: self._a2n[a], aa)
            bbb = map(lambda n: to_one_hot(n, count), nn)
            bbbb.append(bbb)
        return bbbb

    def inverse_transform(self, bbbb):
        aaa = []
        for bbb in bbbb:
            nn = map(lambda bb: from_one_hot(bb), bbb)
            aa = map(lambda n: self._n2a[n], nn)
            aaa.append(aa)
        return aaa
