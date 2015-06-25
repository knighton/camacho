import random


class Batcher(object):
    """
    Keras batches are Theano tensors.  Therefore inputs have to be of the same
    dimensions.  Since we take variable length input sequences, we have to split
    them up by length and chop those up by max_batch_size.
    """

    def __init__(self, max_batch_size):
        assert isinstance(max_batch_size, int)
        assert 1 <= max_batch_size
        self._max_batch_size = max_batch_size

    def make_batches(self, ins_outs):
        """
        in/outs -> numpy arrays of in/out
        """
        len2samples = defaultdict(list)
        for in_out in ins_outs:
            n = len(in_out[0])
            len2samples[n].append(in_out)

        batches = []
        for input_len, ins_outs in len2samples.iteritems():
            for i in range(0, len(ins_outs), max_batch_size):
                sub_ins_outs = np.array(ins_outs[i : i + max_match_size])
                batches.append(sub_ins_outs)

        random.shuffle(batches)

        return batches
