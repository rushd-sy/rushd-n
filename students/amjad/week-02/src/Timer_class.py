from contextlib import contextmanager
import time
class Timer:
    def __enter__(self) -> "Timer":
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        print(f"time: {self.end -self.start}")

@contextmanager
def timer_fun():
    start = time.time()
    yield
    end = time.time()
    print(f"time: {end- start}")



if __name__=="__main__":
    # using context manager function
    with timer_fun():
        sum = 0
        for i in range(1, 1000000):
            sum += i

    print(f"sum: {sum}")



    # using context manager class
    with Timer():
        sum = 0
        for i in range(1, 1000000):
            sum += i

    print(f"sum: {sum}")

