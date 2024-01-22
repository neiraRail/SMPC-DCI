import random


def generateShares(size):
    '''Generates 3 random integer shares of SIZE bytes each'''
    shares = []
    for i in range(3):
        shares.append(int.from_bytes(generateBytes(size), byteorder='big'))
    return shares


def generateBytes(size):
    '''Generates a random bytearray of SIZE bytes'''
    bytes = bytearray()
    for i in range(size):
        bytes.append(random.randint(0, 255))
    
    return bytes