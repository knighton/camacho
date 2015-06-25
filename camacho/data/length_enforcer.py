# There are various ways to enforce length requirements.
#
# TooShortHandler
# * TooShortDropHandler
# * TooShortZeroPadHandler
# * TooShortDieHandler
#
# TooLongHandler
# * TooLongKeepFrontHandler
# * TooLongKeepEdgesHandler
# * TooLongKeepEdgesMostlyFrontHandler
# * TooLongDieHandler
#
# LengthEnforcer


class TooShortHandler(object):
    def __init__(self, min_len):
        self._min_len = min_len

    def is_too_short(self, nn):
        return len(nn) < self._min_len

    def handle(self, nn):
        raise NotImplementedError


class TooShortDropHandler(TooShortHandler):
    def handle(self, nn):
        return None


class TooShortZeroPadHandler(TooShortHandler):
    def handle(self, nn):
        return nn + [0] * (self._min_len - len(nn))


class TooShortException(Exception):
    pass


class TooShortDieHandler(TooShortHandler):
    def handle(self, nn):
        raise TooShortException(
            'Length too short (%d < %d).' % (len(nn), self._min_len)))


class TooLongHandler(object):
    def __init__(self, max_len):
        self._max_len = max_len

    def is_too_long(self, nn):
        return self._max_len < len(nn)

    def handle(self, nn):
        raise NotImplementedError


class TooLongDropHandler(TooLongHandler):
    def handle(self, nn):
        return None


class TooLongKeepFrontHandler(TooLongHandler):
    def handle(self, nn):
        return nn[:self._max_len]


class TooLongKeepEdgesHandler(TooLongHandler):
    def __init__(self, max_len):
        super(TooLongHandler, self).__init__(max_len)
        self._front_len = max_len / 2
        excess = max_len % 2
        if excess:
            self._back_len = max_len / 2
        else:
            self._back_len = max_len / 2 - 1

    def handle(self, nn):
        front = nn[:self._front_len]
        back = nn[-self._back_len:]
        return front + [0] + back


class TooLongKeepEdgesMostlyFrontHandler(TooLongHandler):
    def __init__(self, max_len):
        super(TooLongHandler, self).__init__(max_len)
        excess = max_len % 3
        if not excess:
            self._front_len = max_len * 2 / 3
            self._back_len = max_len / 3 - 1
        elif excess == 1:
            self._front_len = max_len * 2 / 3
            self._back_len = max_len / 3
        else:
            self._front_len = max_len * 2 / 3 + 1
            self._back_len = max_len / 3

    def handle(self, nn):
        front = nn[:self._front_len]
        back = nn[-self.back_len:]
        return front + [0] + back


class TooLongException(Exception):
    pass


class TooLongDieHandler(TooShortHandler):
    def handle(self, nn):
        raise TooLongException(
            'Length too long (%d < %d).' % (self._max_len, len(nn)))


class LengthEnforcer(object):
    """
    Takes various actions if an input sequences is too short or too long.

    Optionally pads ends of sequences so that they line up better (for more
    even batch sizes).
    """

    def __init__(self, too_short, too_long, multiple_of):
        assert isinstance(too_short, TooShortHandler)
        self._too_short = too_short

        assert isinstance(too_long, TooLongHandler)
        self._too_long = too_long

        if multiple_of is not None:
            assert isinstance(multiple_of, int)
            assert 1 <= multiple_of
        self._multiple_of = multiple_of

    def handle(self, nn):
        if self._too_short.is_too_short(nn):
            rr = self._too_short.handle(nn)
        elif self._too_long.is_too_long(nn):
            rr = self._too_long.handle(nn)
        else:
            rr = nn

        if self._multiple_of is not None:
            overhang = len(rr) % self._multiple_of
            rr += [0] * (self._multiple_of - overhang)

        return rr
