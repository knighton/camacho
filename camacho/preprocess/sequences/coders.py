from camacho.base import ReversibleTransformerMixin
from collections import defaultdict


class IntCoder(ReversibleTransformerMixin):
    """
    Converts tokens <-> contiguous range of ints.
    """

    def __init__(self, min_freq=0, top_n=10000, use_oov=True, oov_token=''):
        # Drop the tokens that occur less than min_freq times.
        assert 0 <= min_freq
        self._min_freq = min_freq

        # Drop the tokens that aren't in the top 'top_n' ordered by frequency.
        assert 0 <= top_n
        self._top_n = top_n

        # If you know that the input to fit() will contain all the unique tokens
        # that will ever exist, don't add an OOV token.  Else, do add one.
        assert isinstance(use_oov, bool)
        self._use_oov = use_oov

        # The token to pick when we reverse-transform an unknown integer.
        self._oov_token = oov_token

        # Don't change this without updating fit().
        self._oov_int = 0

    def fit(self, aaa):
        # Count tokens.
        a2count = defaultdict(int)
        for aa in aaa:
            for a in aa:
                a2count[a] += 1

        # Order tokens by frequency.
        counts_aa = []
        for a, count in a2count.iteritems():
            counts_aa.append((count, a))
        counts_aa.sort(reverse=True)

        # Maybe just keep the top n.
        if self._top_n:
            counts_aa = counts_aa[:self._top_n]

        # Maybe pretend too-infrequent tokens are out-of-vocabulary.
        if self._min_freq:
            i = 0
            while i < len(counts_aa):
                count, _ = counts_aa[i]
                if count < self._min_freq:
                    break
                i += 1
            counts_aa = counts_aa[:i]

        # Get the official list of tokens.
        aa = map(lambda (count, a): a, counts_aa)

        # Maybe account for OOV (it maps to zero).
        if self._use_oov:
            i = None
            for i, a in enumerate(aa):
                if a == self._oov_token:
                    break
            if i is None:
                aa = [self._oov_token] + aa[:-1]
            else:
                a = aa[i]
                aa = [a] + aa[:i] + aa[i + 1:]

        # Construct the mapping.
        nn = range(len(aa))
        self._a2n = dict(zip(aa, nn))
        self._n2a = dict(zip(nn, aa))

        return self

    def fit_transform(self, aaa):
        self.fit(aaa)
        return self.transform(aaa)

    def transform(self, aaa):
        nnn = []
        if self._use_oov:
            for aa in aaa:
                nn = map(lambda a: self._a2n.get(a, self._oov_int), aa)
                nnn.append(nn)
        else:
            for aa in aaa:
                nn = map(lambda a: self._a2n[a], aa)
                nnn.append(nn)
        return nnn

    def inverse_transform(self, nnn):
        aaa = []
        for nn in nnn:
            aa = map(lambda n: self._n2a[n], nn)
            aaa.append(aa)
        return aaa
