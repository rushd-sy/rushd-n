def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__} with args: {args} {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add_one(num: int) -> int:
    return num + 1

@log_calls
def add_two(num: int) -> int:
    return num + 2

@log_calls
def greet_user(username: str) -> str:
    return f"Hello, {username}"

print(add_one(4))
print(add_two(8))
print(greet_user("Bitar"))
