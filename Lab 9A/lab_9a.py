import queue

class Node:
    def __init__(self, prio, data):
        self.prio = prio
        self.data = data
    def __lt__(self, other):
        return self.prio<other.prio 
    def __str__(self):
        return "({} {})".format(self.prio, self.data)



def printAndPop(pq):
    while pq.qsize()>0:
        print( pq.get() )
    
def test1():
    print("running test 1")
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