import math
import random
import zlib

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

def entropi(prob):
    H = 0
    for i in prob:
        if i != 0:
            H += i * (math.log((1/i),2))
    return H

def count(arr):
    sum = 0
    for x in arr:
        if x != 0:
            sum += 1
    return sum

bytearr = one()
theCopy = bytearray(len(bytearr))
for i in range(0,len(bytearr)):
    theCopy[i] = bytearr[i]
    
random.shuffle(theCopy)

print("The original:")
print(entropi(makeProb(makeHisto(bytearr))))
print("The shuffled copy:")
print(entropi(makeProb(makeHisto(theCopy))))

code = zlib.compress(theCopy)
print("The uncompressed copy:")
print(len(theCopy))
print("The compressed copy:")
print(len(code))

edoc = zlib.compress(bytearr)
print("The uncompressed original:")
print(len(bytearr))
print("The compressed original:")
print(len(edoc))

t1 = """I hope this lab never ends because
        it is so incredibly thrilling!"""
t10 = 10*t1

t2 = bytearray(t1,'ASCII')
t20 = bytearray(t10,'ASCII')

t3 = zlib.compress(t2)
t30 = zlib.compress(t20)

print("Last part:")
print(len(t2))
print(len(t3))
print(len(t20))
print(len(t30))


