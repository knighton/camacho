from camacho.base import Transformer


class LowerCase(Transformer):
    """
    Convert to lower case.
    """

    def transform(self, texts):
        return map(lambda s: s.lower(), texts)
