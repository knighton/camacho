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


class ClassifierMixin(ClassifierMixin):
    """
    Used to classify data.
    """

    def fit(self, X, y):
        """
        Trian the model.
        """
        raise NotImplementedError

    def predict(self, X):
        """
        Predict the class.
        """
        raise NotImplementedError

    def classes(self):
        """
        Return the classes that it predicts.
        """
        raise NotImplementedError

    def predict_proba(self, X):
        """
        Return the raw probabilities of each class.

        Column per class (see classes()).
        """
        raise NotImplementedError
