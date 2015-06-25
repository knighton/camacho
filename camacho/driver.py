import hashlib
import json
import os


class Driver(object):
    """
    Lightweight controller process that keeps its state in a hierarchy of files.
    Manages the training of models/exploration of model hyperparameters.
    
    - checksum.txt
    - config.json
    - data.txt 
    - models/
        - (model number)/
            - config.json
            - data.json
            - (checkpoint name).hdf5
            - (many checkpoints...)
        - (more models...)
    """

    def __init__(self, dir_name):
        assert os.path.isdir(dir_name)

        fn = os.path.join(dir_name, 'checksum.txt')
        with open(fn) as f:
            checksum = f.read().strip()

        sha1 = hashlib.sha1()

        fn = os.path.join(dir_name, 'config.json')
        with open(fn) as f:
            s = f.read()
        sha1.update(s)
        config = json.loads(s)

        fn = os.path.join(dir_name, 'data.txt')
        with open(fn) as f:
            s = f.read()
        sha1.update(s)

        assert sha1.hexdigest() == checksum

    @staticmethod
    def setup(all_sequences_labels, driver_config, dir_name):
        # Verify it doesn't already exist.
        assert not os.path.exists(dir_name)

        # Set up directories.
        os.makedirs(dir_name)
        os.makedirs(os.path.join(dir_name, 'models'))

        sha1 = hashlib.sha1()

        # Dump config to a file.
        fn = os.path.join(dir_name, 'config.json')
        with open(fn, 'wb') as f:
            s = json.dumps(driver_config, indent=4)
            f.write(s)
            sha1.update(s)

        # Dump original data to a file.
        fn = os.path.join(dir_name, 'data.txt')
        lines = []
        for sequence, label in all_sequences_labels:
            assert isinstance(sequence, (str, unicode))
            assert isinstance(label, (str, unicode))
            j = {
                'text': sequence,
                'label': label,
            }
            line = json.dumps(j) + '\n'
            lines.append(line)
        s = ''.join(lines)
        with open(fn, 'wb') as f:
            f.write(s)
            sha1.update(s)

        # Finally, note our checksum for sanity checking.
        fn = os.path.join(dir_name, 'checksum.txt')
        with open(fn, 'wb') as f:
            f.write(sha1.hexdigest() + '\n')

        return Driver(dir_name)
