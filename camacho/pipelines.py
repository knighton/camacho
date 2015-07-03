from camacho.base import TransformerMixin


class TransformerPipeline(TransformerMixin):
    def __init__(self, steps):
        self._steps = steps

    def fit(self, aa):
        for step in self._steps[:-1]:
            aa = step.fit_transform(aa)
        if self._steps:
            self._steps[-1].fit(aa)
        return self

    def fit_transform(self, aa):
        for step in self._steps:
            aa = step.fit_transform(aa)
        return aa

    def transform(self, aa):
        for step in self._steps:
            aa = step.transform(aa)
        return aa


class ReversibleTransformerPipeline(TransformerPipeline):
    def inverse_transform(self, aa):
        for step in reversed(self._steps):
            aa = step.inverse_transform(aa)
        return aa
