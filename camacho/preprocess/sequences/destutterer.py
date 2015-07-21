from camacho.base import Transformer


class SequenceDestutterer(Transformer):
    """
    Drop overly-repeated items.
    """

    def __init__(self, max_consec=3, ignore=None):
        if ignore is None:
            ignore = []
        self._max_consec = max_consec
        self._ignore = set(ignore)

    def transform(self, aaa):
        rrr = []
        for aa in aaa:
            if not aa:
                rrr.append(aa)
                continue

            rr = []
            prev_a = aa[0]
            run_length = 1
            for i in xrange(1, len(aa)):
                a = aa[i]

                # Different character, or the same character but an 'ignore'?
                # Reset to it.
                if a != prev_a or a in self._ignore:
                    rr.append(a)
                    prev_a = a
                    continue

                # A repeat character but not at the limit?  Keep it.
                run_length += 1
                if run_length <= self._max_consec:
                    rr.append(a)
                    continue

                # Repeated too many times?  Drop it.
            rrr.append(rr)
        return rrr
