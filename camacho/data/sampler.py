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

    def to_d(self):
        return {
            'max_samples_per_class': self._max_samples_per_class,
            'max_spread_ratio': self._max_spread_ratio,
        }

    def sample(self, inputs_classes, num_unique_classes):
        # Shuffle the inputs.
        aa = list(inputs_classes)
        random.shuffle(aa)

        # Separate the inputs by class.
        class2inputs = {}
        for klass in xrange(num_unique_classes):
            class2inputs[klass] = []
        for the_input, klass in aa:
            class2inputs[klass].append(the_input)

        # Get the number of samples we have per class.
        min_num_samples = None
        max_num_samples = None
        for inputs in class2inputs.itervalues():
            n = len(inputs)
            if min_num_samples is None or n < min_num_samples:
                min_num_samples = n
            if max_num_samples is None or max_num_samples < n:
                max_num_samples = n

        # Apply my restrictions on the number of samples allowed per class.
        max_num_samples = min(max_num_samples, self._max_samples_per_class)
        max_num_samples = min(
            max_num_samples, min_num_samples * self._max_spread_ratio)

        # Extract as many comments as we are allowed to per class (they were
        # shuffled in the first step).
        rr = []
        for klass, inputs in class2inputs.iteritems():
            for the_input in inputs[:max_num_samples]:
                rr.append((the_input, klass))

        # Now, shuffle the selected comments.
        random.shuffle(rr)

        return rr


class SamplerCreator(object):
    def from_d(self, d):
        return Sampler(d['max_samples_per_class'], d['max_spread_ratio'])
