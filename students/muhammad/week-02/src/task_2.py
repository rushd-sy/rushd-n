from time import perf_counter, sleep
from contextlib import contextmanager


class timer:
    def __enter__(self):    
        self.start = perf_counter()
    
    def __exit__(self, *_):
        end = perf_counter()
        
        print(f"total time: {end - self.start}")
        

print("First method:")
with timer():
    print("Beginning")
    for i in range(10000):
        # print(i)
        pass
    sleep(2)
    print("End")



@contextmanager
def timer2():
    start = perf_counter()
    
    try:
        yield
    finally:
        print(f"total time: {perf_counter() - start}")

print("\n\nSecond method:")
with timer2():
    print("Beginning")
    for i in range(10000):
        # print(i)
        pass
    sleep(2)
    print("End")
