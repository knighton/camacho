import random


class Batcher(object):
    """
    Keras batches are Theano tensors.  Therefore inputs have to be of the same
    dimensions.  Since we take variable length input sequences, we have to do
    something about that (ie, padding and grouping).
    """

    def __init__(self, min_training_batch_size=96, max_training_batch_size=128):
        assert isinstance(min_training_batch_size, int)
        assert isinstance(max_training_batch_size, int)
        assert 1 <= min_training_batch_size <= max_training_batch_size
        self._min_training_batch_size = min_training_batch_size
        self._max_training_batch_size = max_training_batch_size

    def make_training_batches(self, sequences_classes):
        """
        list of (sequence, class) -> list of (padded sequences, classes)

        Divide the input data into training batches of fairly regular length.
        The drawback is it requires irregular amounts of padding.
        """
        # Sort by sequence length.
        lens_seqs_classes = []
        for seq, klass in sequences_classes:
            length = len(seq)
            lens_seqs_classes.append((length, seq, klass))
        lens_seqs_classes.sort()

        # Divide the inputs into 'min_training_batch_size'-sized chunks.
        #
        # So much for being clever.
        batch_size = self._min_training_batch_size
        batches = []
        for i in range(0, len(lens_seqs_classes), batch_size):
            sub = lens_seqs_classes[i : i + batch_size]
            max_seq_len = sub[-1][0]
            batch_seqs = []
            batch_classes = []
            for seq_len, seq, klass in sub:
                seq_padding = [0] * (max_seq_len - seq_len)
                batch_seqs.append(seq + seq_padding)
                batch_classes.append(klass)
            batch_seqs = np.array(batch_seqs)
            batches.append((batch_seqs, batch_classes))

        # Randomize batch order.
        random.shuffle(batches)

        return batches

    def make_evaluation_batches(self, sequences):
        """
        list of sequence -> (list of list of sequence, list of orig index)

        Group the sequences by length.  Remember the original order.  We don't
        mind irregular batch size when we aren't training.
        """
        # Group sequences by length.
        len2indexes_seqs = defaultdict(list)
        for i, seq in enumerate(sequences):
            len2indexes_seqs[len(seq)].append((i, seq))

        # Extract sequence lists as numpy arrays (while remembering the original
        # order).
        batches = []
        orig_xx = []
        for indexes_seqs in len2indexes_seqs.itervalues():
            seqs = []
            for orig_x, seq in indexes_seqs:
                orig_xx.append(orig_x)
                seqs.append(seq)
            batches.append(np.array(seq)

        return batches, orig_xx
