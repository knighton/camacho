from camacho.base import TransformerMixin
import unicodedata


class LowerCaseNormalizer(TransformerMixin):
    name = 'lower_case_normalizer'

    def fit(self, texts):
        return self

    def fit_transform(self, texts):
        return map(lambda s: s.lower, texts)

    def transform(self, texts):
        return map(lambda s: s.lower, texts)


class UnicodeNormalizer(TransformerMixin):
    name = 'unicode_normalizer'

    def __init__(self, form='nfc'):
        self._form = form

    def fit(self, texts):
        return self

    def fit_transform(self, texts):
        return map(lambda s: unicodedata.normalize(self._form, s), texts)

    def transform(self, texts):
        return map(lambda s: unicodedata.normalize(self._form, s), texts)


class WhitespaceNormalizer(TransformerMixin):
    name = 'whitespace_normalizer'

    def fit(self, texts):
        return self

    def fit_transform(self, texts):
        return map(lambda s: u' '.join(s.split()), texts)

    def transform(self, texts):
        return map(lambda s: u' '.join(s.split()), texts)
