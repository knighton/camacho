class TransformerMixin(object):
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
