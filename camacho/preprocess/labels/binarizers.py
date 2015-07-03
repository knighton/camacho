from camacho.base import ReversibleTransformerMixin
from camacho.util import to_one_hot, from_one_hot


def dict_from_list(aa):
    aa = sorted(set(aa))
    nn = range(len(aa))
    a2n = dict(zip(aa, nn))
    n2a = dict(zip(nn, aa))
    return a2n, n2a


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
        nn = map(from_one_hot, nnn)
        return map(lambda n: self._n2a[n], nn)
