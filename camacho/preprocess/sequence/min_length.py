from camacho.base import Transformer


class ExtendHandler(object):
    def __init__(self, min_len, pad_token):
        raise NotImplementedError

    def extend(self, aa):
        raise NotImplementedError


class PadFront(ExtendHandler):
    def __init__(self, min_len, pad_token):
        self._min_len = min_len
        self._pad_token = pad_token

    def extend(self, aa):
        n = self._min_len - len(aa)
        return ''.join([self._pad_token] * n) + aa


class PadBack(ExtendHandler):
    def __init__(self, min_len, pad_token):
        self._min_len = min_len
        self._pad_token = pad_token

    def extend(self, aa):
        n = self._min_len - len(aa)
        return aa + ''.join([self._pad_token] * n)


EXTEND_HANDLERS = [
    PadFront,
    PadBack,
]


ACTION2HANDLER = {}
for klass in EXTEND_HANDLERS:
    ACTION2HANDLER[klass.__name__] = klass


class MinLength(Transformer):
    def __init__(self, min_len=0, action='PadBack', pad_token='\0'):
        self._min_len = min_len
        self._action = action
        self._pad_token = pad_token
        self._extender = ACTION2HANDLER[action](min_len, pad_token)

    def transform(self, aaa):
        rrr = []
        for aa in aaa:
            if self._min_len <= len(aa):
                rr = aa
            else:
                rr = self._extender.extend(aa)
            rrr.append(rr)
        return rrr
