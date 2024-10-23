import queue

class Node:
    def __init__(self, prio, data):
        self.prio = prio
        self.data = data
    def __lt__(self, other):
        return self.prio<other.prio 
    def __str__(self):
        return "({} {})".format(self.prio, self.data)
    
def one():
    file = open(r"Lab 9\exempeltext.txt", "r")
    txt = file.read()
    byteArr = bytearray(txt, "utf-8")
    return byteArr
    
def makeHisto(byteArr):
    histogram = [0] * 256
    for byte in byteArr:
        histogram[byte] += 1
    return histogram

def makeProb(histo):
    sum = 0
    norm = [0.0] * 256
    for n in histo:
        sum += n
    for x in range(0,256):
        norm[x] = histo[x] / sum
    return norm

def printAndPop(pq):
    while pq.qsize()>0:
        print( pq.get() )

def test1():
    norm = makeProb(makeHisto(one()))
    pq = queue.PriorityQueue()
    pq.put( Node(4.0, 10) )
    pq.put( Node(2.0, 8) )
    pq.put( Node(5.0, 2) )
    pq.put( Node(1.5, 8) )
    pq.put( Node(4.0, 8) )
    pq.put( Node(1.0, 8) )
    pq.put( Node(3.0, (1,2)) )
    pq.put( Node(2.0, (1,2)) )
    printAndPop( pq)
test1()