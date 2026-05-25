from itertools import islice

def fibo():
    a = 0
    b = 1
    while a < 20:
        yield a
        a, b = b, b + a
    yield a
    yield b

fibo_seq_with_itertools = list(islice(fibo(), 20))
