def logs_call(func) :
    def wrapper(*args, **kwargs) -> None:
        print(f"name: {func.__name__}")
        print(f"kwargs: {kwargs}")
        print(f"args: {args}")
        return func(*args, **kwargs)
    return wrapper

@logs_call
def add(a: int, b: int, *args, **kwargs) -> int:
    return a + b

if __name__ == "__main__":
    print(add(2, 3, name="Amjad", age=25))