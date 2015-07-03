from collections import defaultdict
import numpy as np


def v2k_from_k2v(k2v):
    v2k = {}
    for k, v in k2v.iteritems():
        assert v not in v2k
        v2k[v] = k
    return v2k


def v2kk_from_k2v(k2v):
    v2kk = defaultdict(list)
    for k, v in k2v.iteritems():
        v2kk[v].append(k)
    return v2kk


def to_one_hot(x, length):
    bb = [0] * length
    bb[x] = 1
    return bb


def ones_and_zeros(one_indexes, length):
    bb = [0] * length
    for x in one_indexes:
        bb[x] = 1
    return bb


def from_one_hot(bb):
    return np.argmax(bb)


def import_path_from_object(obj):
    return obj.__module__ + '.' + obj.__class__.__name__


def import_path_from_class(klass):
    return klass.__module__ + '.' + klass.__name__


def class_from_import_path(path):
    x = path.rindex('.')
    module_path = path[:x]
    class_name = path[x + 1:]
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)
