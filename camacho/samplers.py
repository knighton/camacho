from collections import defaultdict
import logging
import random


class Sampler(object):
    def sample(self, aa):
        raise NotImplementedError


class CountSampler(Sampler):
    name = 'count_sampler'

    def __init__(self, train_per_class=5000, val_per_class=3000,
                 test_per_class=3000):
        self._train_per_class = train_per_class
        self._val_per_class = val_per_class
        self._test_per_class = test_per_class

    def sample(self, ins_outs):
        out2ins = defaultdict(list)
        for the_input, output in ins_outs:
            out2ins[output].append(the_input)

        logging.info('Data points: %d.' % len(ins_outs))
        logging.info('Counts per class:')
        for out, ins in out2ins.iteritems():
            logging.info('%s -> %d' % (out, len(ins)))

        a = self._train_per_class
        b = self._val_per_class
        c = self._test_per_class
        trains = []
        vals = []
        tests = []
        for out, ins in out2ins.iteritems():
            assert a + b + c <= len(ins)
            random.shuffle(ins)
            train = ins[:a]
            trains.extend(train)
            val = ins[a : a + b]
            vals.extend(val)
            test = ins[a + b : a + b + c]
            tests.extend(test)

        random.shuffle(trains)
        random.shuffle(vals)
        random.shuffle(tests)

        return trains, vals, tests


class ProportionalSampler(Sampler):
    name = 'proportional_sampler'

    def __init__(self, num_train=10000, num_val=5000, num_test=5000):
        self._num_train = num_train
        self._num_val = num_val
        self._num_test = num_test

    def sample(self, ins_outs):
        a = self._num_train
        b = self._num_val
        c = self._num_test
        assert a + b + c <= len(ins_outs)
        aa = list(ins_outs)
        random.shuffle(aa)
        trains = ins_outs[:a]
        vals = ins_outs[a : a + b]
        tests = ins_outs[a + b : a + b + c]
        return trains, vals, tests
