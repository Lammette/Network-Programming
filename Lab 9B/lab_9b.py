import queue

class Node:
    def __init__(self, prio, data):
        self.prio = prio
        self.data = data
    def __lt__(self, other):
        return self.prio<other.prio 
    def __str__(self):
        return "({} {})".format(self.prio, self.data)
    
def fileToByte():
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
        
def req(x,n):
    global codelength           #Add to average codelength
    if type(n.data) == int:
        length = len(bin(x))    #Depth of tree = bits needed to present symbol (not ASCII anymore)
        print(length)
        codelength += (n.prio * length) #Average codelength = Sum(probability*codelength)
        return
    else:
        left, right = n.data    # Get child nodes
        req((x+1),left)         # depth first
        req((x+1),right)


def transform():
    arr = fileToByte()  #Bytearray
    norm = makeProb(makeHisto(arr)) #Histogram -> Probability
    pq = queue.PriorityQueue()
    for p,b in zip(norm, range(0,256)): #Add all symbols used
        if p != 0:
            pq.put(Node(p,b))
            
    while pq.qsize() != 1:      #Huffman encoding
        #Take 2 lowest probability leaves and bind them to a node
        #  Queue    >      Node
        #   []              O
        #   []            /   \
        #   []           O     O
        left = pq.get()
        right = pq.get()
        
        pq.put(Node(left.prio + right.prio,(left,right)))   #Put back into queue
        
    # pq is now a huffman encoded tree
    
    #Calculate average codelength
    req(0,pq.get())
    
    print(codelength)
    
codelength = 0
transform()