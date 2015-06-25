import random


class Sampler(object):
    """
    Selects up to 'max_samples_per_class' samples per class, limited by the fact
    that the highest sample countmust be witin 'max_spread_ratio' of the lowest
    sample count.
    """

    def __init__(self, max_samples_per_class=10000, max_spread_ratio=2.0):
        self._max_samples_per_class = max_samples_per_class
        self._max_spread_ratio = max_spread_ratio

    def sample(self, inputs_classes, num_unique_classes):
        aa = list(inputs_classes)
        
        random.shuffle(aa)

        class2inputs = {}
        for klass in xrange(num_unique_classes):
            class2inputs[klass] = []

        for the_input, klass in aa:
            class2inputs[klass].append(the_input)

        min_num_samples = None
        max_num_samples = None
        for inputs in class2inputs.itervalues():
            n = len(inputs)
            if min_num_samples is None or n < min_num_samples:
                min_num_samples = n
            if max_num_samples is None or max_num_samples < n:
                max_num_samples = n

        max_num_samples = min(max_num_samples, self._max_samples_per_class)

        max_num_samples = min(
            max_num_samples, min_num_samples * self._max_spread_ratio)

        rr = []
        for klass, inputs in class2inputs.iteritems():
            for the_input in inputs[:max_num_samples]:
                rr.append((the_input, klass))

        random.shuffle(rr)

        return rr
