from camacho.base import TransformerMixin


class LowerCase(TransformerMixin):
    """
    Convert to lower case.
    """

    def transform(self, texts):
        return map(lambda s: s.lower(), texts)
