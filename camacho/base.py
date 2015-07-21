class Transformer(object):
    """
    Used to preprocess/postprocess data.

    Classifier example:

        [data, labels]
            |--transform()
            v
        [binary data, labels for training]

            then

        [data]
            |--transform()
            v
        [binary data for evaluation]
            |--classify()
            v
        [binary labels]
            |--inverse_transform()
            v
        [labels]

    Autoencoder example:

        [data]
            |--transform()
            v
        [binary data]
            |--encode()
            v
        [smaller binary data]
            |--decode()
            v
        [recreated binary data]
            |--inverse_transform()
            v
        [data]
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
        self.fit(aa)
        return self.transform(aa)

    def transform(self, aa):
        """
        items -> transformed items
        """
        raise NotImplementedError

    def inverse_transform(self, aa):
        """
        transformed items -> items
        """
        raise NotImplementedError


class ClassifierMixin(object):
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
