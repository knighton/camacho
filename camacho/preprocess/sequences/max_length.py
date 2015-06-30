from camacho.base import TransformerMixin


class TruncateHandler(object):
    def __init__(self, max_len, divider_token):
        raise NotImplementedError

    def truncate(self, aa):
        raise NotImplementedError


class TruncateEnd(TruncateHandler):
    name = 'truncate_end'

    def __init__(self, max_len, divider_token):
        self._max_len = max_len

    def truncate(self, aa):
        return aa[:self._max_len]


class TruncateMiddle(TruncateHandler):
    name = 'truncate_end'

    def __init__(self, max_len, divider_token):
        excess = max_len % 2
        if excess:
            self._front_len = max_len / 2
            self._back_len = max_len / 2
        else:
            self._front_len = max_len / 2
            self._back_len = max_len / 2 - 1
        self._divider_token = divider_token

    def truncate(self, aa):
        front = aa[:self._front_len]
        back = aa[-self._back_len:]
        return front + [self._divider_token] + back


class TruncateMidBack(TruncateHandler):
    name = 'truncate_mid_back'

    def __init__(self, max_len, divider_token):
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
        self._divider_token = divider_token

    def truncate(self, aa):
        front = aa[:self._front_len]
        back = aa[-self._back_len:]
        return front + [self._divider_token] + back


TRUNCATE_HANDLERS = [
    TruncateEnd,
    TruncateMiddle,
    TruncateMidBack,
]


ACTION2HANDLER = {}
for klass in TRUNCATE_HANDLERS:
    ACTION2HANDLER[klass.name] = klass


class MaxLengthEnforcer(TransformerMixin):
    name = 'max_length_enforcer'

    def __init__(self, max_len=512, action='truncate_mid_back',
                 divider_token='\0'):
        self._max_len = max_len
        self._action = action
        self._divider_token = divider_token
        self._truncator = ACTION2HANDLER[action](max_len, divider_token)
        self._fitted = False

    def fit(self, aaa):
        self._fitted = True
        return self

    def fit_transform(self, aaa):
        self.fit()
        return self.transform(aaa)

    def transform(self, aaa):
        rrr = []
        for aa in aaa:
            if len(aa) <= self._max_len:
                rr = aa
            else:
                rr = self._truncator.truncate(aa)
            rrr.append(aa)
        return rrr
