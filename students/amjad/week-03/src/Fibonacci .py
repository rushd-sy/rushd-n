from itertools import islice


def Fibonacci():
    a: int = 0
    b: int = 1
    yield a
    while True:
        yield b
        a = b
        b = a + b


if __name__ == "__main__":
    for num in islice(Fibonacci(), 20):
        print(num)
