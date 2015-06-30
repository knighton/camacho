class TransformerMixin(object):
    def fit(self, aa):
        """
        items -> self
        """
        raise NotImplementedError

    def fit_transform(self, aa):
        """
        items -> transformed items
        """
        raise NotImplementedError

    def transform(self, aa):
        """
        items -> transformed items
        """
        raise NotImplementedError
