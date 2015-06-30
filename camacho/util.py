def v2k_from_k2v(k2v):
    v2k = {}
    for k, v in k2v.iteritems():
        v2k[v] = k
    return v2k
