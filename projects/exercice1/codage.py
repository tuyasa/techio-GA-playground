import random
from solution import alphabet

def get_letter():
    return ord(random.choice(alphabet))

def creer_chromosome(size):
    return bytearray()
    