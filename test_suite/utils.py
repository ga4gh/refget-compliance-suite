class Sequence:
    '''Sequence model object used to store seqeunce data in a defined manner
    '''
    def __init__(self, name, sequence, is_circular, sha512, md5, size):
        self.name = name
        self.sequence = sequence
        self.is_circular = is_circular
        self.sha512 = sha512
        self.md5 = md5
        self.size = size


# Additional utility functions to load the sequence data


def read_sequence(chr_name):
    sequence_file = open("test_chromosomes/" + chr_name + ".txt", "r")
    sequence_data = sequence_file.read().replace('\n', '')
    return sequence_data


def get_seq_obj(chr):
    if chr is "I":
        return Sequence(
            'I',
            read_sequence(chr),
            False,
            '959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7',
            '6681ac2f62509cfc220d78751b8dc524',
            len(read_sequence(chr))
        )
    if chr is "VI":
        return Sequence(
            'VI',
            read_sequence(chr),
            False,
            'cfea89816a1a711055efbcdc32064df44feeb6b773990b07',
            'b7ebc601f9a7df2e1ec5863deeae88a3',
            len(read_sequence(chr))
        )
    else:
        return Sequence(
            'NC',
            read_sequence(chr),
            True,
            '2085c82d80500a91dd0b8aa9237b0e43f1c07809bd6e6785',
            '3332ed720ac7eaa9b3655c06f6b9e196',
            len(read_sequence(chr))
        )
