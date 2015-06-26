# Classes:
#
# - Encoder
#   - AutoLabelEncoder
#   - ManualLabelEncoder
#   - SequenceEncoder


from collections import defaultdict


class Encoder(object):
    """
    A mapping of some vocabulary to contiguous integers.
    """

    def vocab_size(self):
        raise NotImplementedError

    def fit(self, aa):
        raise NotImplementedError

    def encode(self, a):
        raise NotImplementedError

    def decode(self, a):
        raise NotImplementedError


def assign_ints_by_freq(a2count, add_unk):
    count2aa = defaultdict(list)
    for a, count in a2count.iteritems():
        count2aa[count].append(a)

    a2n = {}
    n2a = {}
    for count in sorted(count2aa, reversed=True):
        for a in sorted(count2aa[count]):
            if add_unk:
                n = len(a2n) + 1
            else:
                n = len(a2n)
            a2n[a] = n
            n2a[n] = a

    return a2n, n2a


class AutoLabelEncoder(Encoder):
    def __init__(self):
        self._label2n = {}
        self._n2label = {}

    def vocab_size(self):
        return len(self._label2n)

    def fit(self, labels):
        label2count = defaultdict(int)
        for a in aa:
            label2count[a] += 1

        self._label2n, self._n2label = assign_ints_by_freq(
            label2count, add_unk=False)

    def encode(self, label):
        return self._label2n[label]

    def decode(self, n):
        return self._n2label[n]


class ManualLabelEncoder(Encoder):
    def __init__(self, ordered_labels):
        for label in ordered_labels:
            assert isinstance(label, (str, unicode))

        self._label2n = dict(zip(ordered_labels, xrange(len(ordered_labels))))
        self._n2label = dict(zip(xrange(len(ordered_labels)), ordered_labels))

    def vocab_size(self):
        return len(self._label2n)

    def fit(self, labels):
        for label in labels:
            assert label in self._label2n

    def encode(self, label):
        return self._label2n[label]

    def decode(self, n):
        return self._n2label[n]


class SequenceEncoder(Encoder):
    def __init__(self, min_freq):
        if min_freq is not None:
            assert 1 <= min_freq
            assert isinstance(min_freq, int)
        self._min_freq = min_freq

        self._a2n = {}
        self._n2a = {}

    def vocab_size(self):
        return len(self._a2n) + 1

    def fit(self, aaa):
        # Count characters, tokens, etc.
        a2count = defaultdict(int)
        for aa in aaa:
            for a in aa:
                a2count[a] += 1

        # Drop the ones that are too infrequent (will be replaced with unk).
        if self_min_freq is not None:
            for a, count in a2count.items():
                if count < self._min_freq:
                    del a2count[a]

        # Number the unique items by their frequency of occurence.
        self._a2n, self._n2a = assign_ints_by_freq(a2count, add_unk=True)

    def encode(self, aa):
        return map(lambda a: self._a2n.get(a, 0), aa)

    def decode(self, nn):
        return map(lambda n: self._n2a[n], nn)
