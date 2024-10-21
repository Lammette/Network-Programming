import random
suit = ["spades","hearts","diamonds","clubs"]
value = ["two","three","four","five","six","seven","eight","nine","ten","jack","queen","king","ace"]

class Card:
    def __init__(self, suit, value):
        assert 1 <= suit <= 4 and 1 <= value <= 13
        self._suit = suit
        self._value = value
    def getValue(self):
        return self._value
    def getSuit(self):
        return self._suit
    def __str__(self):
        return value[self._value - 1] +" of "+ suit[self._suit - 1]
        
    
class CardDeck:
    def __init__(self):
        self._deck = []
        self.reset()
    def shuffle(self):
        random.shuffle(self._deck)
    def getCard(self):
        card = self._deck.pop(0)
        return card
    def size(self):
        return len(self._deck)
    def reset(self):
        deck = []
        for s in range(1,5):
            for v in range(1,14):
                deck.append(Card(s,v))
        self._deck = deck


# Test
deck = CardDeck()
deck.shuffle()
while deck.size()>0:
    card = deck.getCard()
    print("Card {} has value {}".format(card, card.getValue()))

deck.reset()
while deck.size()>0:
    card = deck.getCard()
    print("Card {} has value {}".format(card, card.getValue()))

