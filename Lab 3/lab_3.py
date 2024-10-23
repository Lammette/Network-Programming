import random
suit = {1: "spades", 2: "hearts", 3: "diamond", 4:"clubs"}
value = {1:"ace",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten",11:"jack",12:"queen",13:"king"}

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
        return value[self._value] +" of "+ suit[self._suit]
        
    
class CardDeck:
    def __init__(self):
        self._deck = []
        self.reset()
    def shuffle(self):
        random.shuffle(self._deck)
    def getCard(self):
        card = self._deck.pop()
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
print("Shuffled deck")
while deck.size()>0:
    card = deck.getCard()
    print("Card {} has value {}".format(card, card.getValue()))

print("\n\nReset deck")
deck.reset()
while deck.size()>0:
    card = deck.getCard()
    print("Card {} has value {}".format(card, card.getValue()))

