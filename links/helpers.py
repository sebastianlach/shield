from functools import reduce
from random import choice
from string import ascii_letters, digits

def bitwise_or(sequence):
    return reduce(lambda x, y: x | y, sequence)


def generate_token(length=6):
    characters = ascii_letters + digits
    return "".join([choice(characters) for _ in range(length)])
