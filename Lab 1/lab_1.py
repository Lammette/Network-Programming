# 1.3.1
# 1. No
# 2. use //
# 3. 0.5

# 1.3.2
# 1. 'spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam '
# 2. """x       '''x
#       x          x
#       x"""       x'''
# 3. \", """ "x" """, '"x"'
# 4.
#   a. Hello
#   b. Hello
#   c. !
# 5. len(string)
# 6.    s[0] = D  
#       raceback (most recent call last):
#       File "<stdin>", line 1, in <module>
#       NameError: name 'D' is not defined

# 1.3.3
# 1. 
#   a. [99, 1, 2, 3, 4, 5, 6, 7]
#   b. [100, 1, 2]
#   c. [100, 1, 2, 3, 4, 5, 6, 7]
#   d. refer to the same object
# 2. len(list)
# 3. 3

# 1.3.4
# 1. swithes a and b
# 2.
x = 0
while x < 10:
    print(x)
    x += 1

# 1.4.1
# 1. Cause some lazy ass mf

# 1.4.2
# 1.
animal = ["dog", "cat", "elefant"] 
for x in animal:
    print (x)
    
# 2. You want to loop through a copy, it is safer

# 1.4.3
# 1.
for x in range(100):
    print(x) 
# 2.
x = list(range(100))

# 1.4.4
# 1. When the loop is terminated with break

# 1.4.5
# 1. pass

# 1.4.6
# 1.
def hello(n):
    for x in range(n):
        print("parrot")
# 2. refrence to the function
# 3. Local / Global symbol table
# 4. Just use it lol
# 5.
animal.append("flea")

# 1.4.7
# keyword arguments
def print_all(*args, sep="/"):
    return sep.join(args)
# lamda function
# 1. 5
# document string
# 1. print the documentation string
# 2.
def funcmyass():
    """Doc string"""
    pass

# 1.4.8
# 1. 4 spaces
# 2. idfk 32 = space, tab = 4 spaces

#1.5.1
# 1. 
#   a.
a = [1,2,3,1,1,1,5,7,2]
a.count(1) 
#   b. no bitch

# using lists as stack
# [1,2,3]

# using lists as queues
# [3,4,8,9]
# because elements are added at the beginning and everything else has to shift

# list comprehension
a = [0,1,2,3,4,5,6,7,8,9,10]
b = [x**2 for x in a]

# 1.5.2
# 1. b,c,d because tuples are immutable
# 2. unpack the tuple, x = 1111, y = 2222, z = 3333

# 1.5.3
# 1.
x = {"yes","yeah","jop","ok"}
def c(answ):
    if answ in x:
        print ("you answered yes")
# 2.
z = set("Din mamma")
# 3.
ragnar = ["minus","poäng"]
z = set(ragnar)

# 1.5.4
# 1.
for x in ragnar:
    print(x)
# 2.
jerome = {"electronic" : 420, "guy" : 69}
for x, y in jerome.items():
    print(x,y)
    
# 1.5.5
# 1. 
if x in range(20,66):
    print("vad jobbar du med?")
# 2. and

# 1.5.6
# 1. a,c,e

# 1.6.
import prog

prog.getLotto()

# 1.7.1
# 1. 'A=1 och B=2'

# 1.7.2
# 1.
f = open("Lab 1\din_mamma.txt", "r")
print(f.read())

