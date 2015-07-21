from camacho.base import Transformer
from gensim.models.word2vec import Word2Vec as InternalWord2Vec
import numpy as np
from numpy.linalg import norm


def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))


class Word2Vec(Transformer):
    """
    Tokens <-> arrays of float.
    """

    def __init__(self, num_dims=16):
        self._num_dims = num_dims
        self._model = None
        self._index2token = None

    def fit(self, aaa):
        aaa = list(aaa)  # Gensim performs worse on generators.
        self._model = InternalWord2Vec(sentences=aaa, size=self._num_dims)
        self._model.init_sims(replace=True)  # To save memory.
        self._index2token = {}
        for token, entry in self._model.vocab.iteritems():
            self._index2token[entry.index] = token

    def transform(self, aaa):
        ffff = []
        for aa in aaa:
            fff = []
            for a in aa:
                ff = self._model[a]
                fff.append(ff)
            ffff.append(fff)
        return ffff

    def _decode(self, ff):
        sims_xx = []
        other_fff = self._model.syn0
        for x, other_ff in zip(xrange(len(other_fff)), other_fff):
            sim = cosine_similarity(ff, other_ff)
            sims_xx.append((sim, x))
        sims_xx.sort(reverse=True)
        x = sims_xx[0][1]
        return self._index2token[x]

    def inverse_transform(self, ffff):
        aaa = []
        for fff in ffff:
            aa = []
            for ff in fff:
                a = self._decode(ff)
                aa.append(a)
            aaa.append(aa)
        return aaa
