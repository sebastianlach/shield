from functools import reduce


def bitwise_or(sequence):
    return reduce(lambda x, y: x | y, sequence)
