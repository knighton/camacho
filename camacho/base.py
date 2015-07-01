class TransformerMixin(object):
    """
    Used to preprocess data.
    """

    def fit(self, aa):
        """
        items -> self
        """
        return self

    def fit_transform(self, aa):
        """
        items -> transformed items
        """
        self.fit()
        return self.transform(aa)

    def transform(self, aa):
        """
        items -> transformed items
        """
        raise NotImplementedError


class ReversibleTransformerMixin(TransformerMixin):
    """
    Used to encode/decode labels.
    """

    def inverse_transform(self, aa):
        """
        transformed items -> items
        """
        raise NotImplementedError
