import random

def getLotto():
    bajs = set()
    for x in range(7):
        bajs.add(random.randrange(1,35))
