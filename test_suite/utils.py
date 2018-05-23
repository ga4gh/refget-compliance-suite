from chromosome_model import Chromosome


def read_sequence(chr_name):
    sequence_file = open("test_chromosomes/" + chr_name + ".txt", "r")
    sequence_data = sequence_file.read().replace('\n', '')
    return sequence_data


def populate_db():
    I = Chromosome(
        name='I',
        sequence=read_sequence('I'),
        is_circular=0,
        trunc512='959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7',
        md5='6681ac2f62509cfc220d78751b8dc524',
        size=len(read_sequence('I'))
    )
    I.save()
    VI = Chromosome(
        name='VI',
        sequence=read_sequence('VI'),
        is_circular=0,
        trunc512='cfea89816a1a711055efbcdc32064df44feeb6b773990b07',
        md5='b7ebc601f9a7df2e1ec5863deeae88a3',
        size=len(read_sequence('VI'))
    )
    VI.save()
    NC = Chromosome(
        name='NC',
        sequence=read_sequence('NC'),
        is_circular=1,
        trunc512='2085c82d80500a91dd0b8aa9237b0e43f1c07809bd6e6785',
        md5='3332ed720ac7eaa9b3655c06f6b9e196',
        size=len(read_sequence('NC'))
    )
    NC.save()
