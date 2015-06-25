# There are various ways to enforce length requirements.
#
# Classes:
#
# - TooShortHandler
#   - TooShortDropHandler
#   - TooShortZeroPadHandler
#   - TooShortDieHandler
#
# - TooShortHandlerCreator
#
# - TooLongHandler
#   - TooLongKeepFrontHandler
#   - TooLongKeepEdgesHandler
#   - TooLongKeepEdgesMostlyFrontHandler
#   - TooLongDieHandler
#
# - TooLongHandlerCreator
#
# - LengthEnforcer
#
# - LengthEnforcerCreator


class TooShortHandler(object):
    def __init__(self, min_len):
        self._min_len = min_len
        self._policy = None

    def policy(self):
        return self._policy

    def to_d(self):
        return {
            'min_len': self._min_len,
            'policy': self.policy(),
        }

    def is_too_short(self, nn):
        return len(nn) < self._min_len

    def handle(self, nn):
        raise NotImplementedError


class TooShortDropHandler(TooShortHandler):
    def __init__(self, min_len):
        super(TooShortHandler, self).__init__(min_len)
        self._policy = 'drop'

    def handle(self, nn):
        return None


class TooShortZeroPadHandler(TooShortHandler):
    def __init__(self, min_len):
        super(TooShortHandler, self).__init__(min_len)
        self._policy = 'zero_pad'

    def handle(self, nn):
        return nn + [0] * (self._min_len - len(nn))


class TooShortException(Exception):
    pass


class TooShortDieHandler(TooShortHandler):
    def __init__(self, min_len):
        super(TooShortHandler, self).__init__(min_len)
        self._policy = 'die'

    def handle(self, nn):
        raise TooShortException(
            'Length too short (%d < %d).' % (len(nn), self._min_len)))


class TooShortHandlerCreator(object):
    def __init__(self):
        self._classes = [
            TooShortDropHandler,
            TooShortZeroPadHandler,
            TooShortDieHandler,
        ]

        self._policy2class = {}
        for klass in self._classes:
            policy = klass(1337).policy()
            self._policy2class[policy] = klass

    def from_d(self, d):
        policy = d['policy']
        klass = self._policy2class[policy]
        return klass(d['min_len'])


class TooLongHandler(object):
    def __init__(self, max_len):
        self._max_len = max_len
        self._policy = None

    def policy(self):
        return self._policy

    def to_d(self):
        return {
            'max_len': self._max_len,
            'policy': self.policy(),
        }

    def is_too_long(self, nn):
        return self._max_len < len(nn)

    def handle(self, nn):
        raise NotImplementedError


class TooLongDropHandler(TooLongHandler):
    def __init__(self, max_len):
        super(TooLongHandler, self).__init__(max_len)
        self._policy = 'drop'

    def handle(self, nn):
        return None


class TooLongKeepFrontHandler(TooLongHandler):
    def __init__(self, max_len):
        super(TooLongHandler, self).__init__(max_len)
        self._policy = 'keep_front'

    def handle(self, nn):
        return nn[:self._max_len]


class TooLongKeepEdgesHandler(TooLongHandler):
    def __init__(self, max_len):
        super(TooLongHandler, self).__init__(max_len)
        self._policy = 'keep_edges'
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
        self._policy = 'keep_edges_mostly_front'
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
    def __init__(self, max_len):
        super(TooLongHandler, self).__init__(max_len)
        self._policy = 'die'

    def handle(self, nn):
        raise TooLongException(
            'Length too long (%d < %d).' % (self._max_len, len(nn)))


class TooLongHandlerCreator(object):
    def __init__(self):
        self._classes = [
            TooLongDropHandler,
            TooLongKeepFrontHandler,
            TooLongKeepEdgesHandler,
            TooLongKeepEdgesMostlyFrontHandler,
            TooLongDieHandler,
        ]

        self._policy2class = {}
        for klass in self._classes:
            policy = klass(1337).policy()
            self._policy2class[policy] = klass

    def from_d(self, d):
        policy = d['policy']
        klass = self._policy2class[policy]
        return klass(d['max_len'])


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
            assert 2 <= multiple_of
        self._multiple_of = multiple_of

    def to_d(self):
        return {
            'too_short': self._too_short.to_d(),
            'too_long': self._too_long.to_d(),
            'multiple_of': self._multiple_of,
        }

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


class LengthEnforcerCreator(object):
    def __init__(self):
        self._too_short = TooShortHandlerCreator()
        self._too_long = TooLongHandlerCreator()

    def from_d(self, d):
        too_short = self._too_short.from_d(d['too_short'])
        too_long = self._too_long.from_d(d['too_long'])
        multiple_of = d['multiple_of']
        return LengthEnforcer(too_short, too_long, multiple_of)
