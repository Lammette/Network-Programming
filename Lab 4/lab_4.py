
def fibonacci(n):
    a, b = 0, 1
    while b < n:
        yield b
        a, b = b, a + b

for i in fibonacci(1000000):
    print(i)