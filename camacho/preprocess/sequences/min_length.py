from camacho.base import TransformerMixin


class ExtendHandler(object):
    def __init__(self, min_len, pad_token):
        raise NotImplementedError

    def extend(self, aa):
        raise NotImplementedError


class PadFront(ExtendHandler):
    name = 'pad_front'

    def __init__(self, min_len, pad_token):
        self._min_len = min_len
        self._pad_token = pad_token

    def extend(self, aa):
        n = self._min_len - len(aa)
        return [self._pad_token] * n + aa


class PadBack(ExtendHandler):
    name = 'pad_back'

    def __init__(self, min_len, pad_token):
        self._min_len = min_len
        self._pad_token = pad_token

    def extend(self, aa):
        n = self._min_len - len(aa)
        return aa + [self._pad_token] * n


EXTEND_HANDLERS = [
    PadFront,
    PadBack,
]


ACTION2HANDLER = {}
for klass in EXTEND_HANDLERS:
    ACTION2HANDLER[klass.name] = klass


class MinLengthEnforcer(TransformerMixin):
    name = 'min_length_enforcer'

    def __init__(self, min_len=0, action='pad_back', pad_token='\0'):
        self._min_len = min_len
        self._action = action
        self._pad_token = pad_token
        self._extender = ACTION2HANDLER[action](min_len, divider_token)
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
            if self._min_len <= len(aa):
                rr = aa
            else:
                rr = self._extender.extend(aa)
            rrr.append(rr)
        return rrr