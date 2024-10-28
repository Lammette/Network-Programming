import queue
import math

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
    global codewords
    if type(n.data) == int:
        #length = len(format(n.data, 'b'))   #UTF-8 without the zeros
        length = len(x)                     #Hoffman
        codelength += (n.prio * length)     #Average codelength = Sum(probability*codelength)
        codewords[n.data] = x
        word_prio[n.data] = n.prio
        return
    else:
        left, right = n.data    # Get child nodes
        req((x + '0'),left)         # depth first
        req((x + '1'),right)


def transform():
    arr = fileToByte()  #Bytearray
    norm = makeProb(makeHisto(arr)) #Histogram -> Probability
    pq = queue.PriorityQueue()
    for p,b in zip(norm, range(0,256)): #Add all symbols used
        if p:
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
    req('0',pq.get())
    
    print("Avg code length:", codelength)
    
    for x in range (0, 256):            #All ASCII characters
        for b,l in codewords.items():   #All codewords from the hoffman tree
                                        #b = byte in UTF-8 / ASCII
                                        #l = hoffman byte
            if b == x and b >= 32:      #If ASCII character if printable
                print(f"byte= {b}\t({chr(b) if b >= 32 and b <= 127 else ""})\t{l}\t{"\t\t" if len(l) < 8 else "\t" if len(l) < 16 else ""}len={len(l)}\tlog(1/p)={math.log((1/word_prio[x]),2):.2f}")
                
codelength = 0 #Avg code length, sum of all probable codelengths
codewords = {} #List of codewords from hoffman tree
word_prio = {} #Priority for each node in the hoffman tree/codeword
transform()