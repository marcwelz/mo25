# prints string to console
def print_hi(name: str) -> None:
    print(f'Hi, {name}')

# adds two numbers
def add_numbers(a: int, b: int) -> int:
    return a + b

# calculates square root of a number with optional second parameter
def square_root(a: int, b: int | None = None) -> float:
    b = b if b is not None else 2
    return a ** (1 / b)

# rounds down the division of two numbers
def round_to_full_number(a: int, b: int) -> int:
    return a // b

# performs bitwise XOR on two numbers
def xor(a: int, b: int) -> int:
    return a ^ b

# returns the remainder of the division of two numbers
def return_rest_of_division(a: int, b: int) -> int:
    return a % b

# normalizes hour to a 24-hour format
def normalize_hour(a: int) -> int:
    return (23 + a) % 24

# rounds a float to the nearest integer. Important! Always rounds to a even number
def round_function(a: float) -> int:
    return round(a)

def run_all_theory_functions() -> None:
    print_hi('PyCharm')
    print(add_numbers(3, 5))
    print(add_numbers(3, 5), "is the sum of 3 and 5")
    print(square_root(3, 5), "is the square root of 3 and 5")
    print(round_to_full_number(3, 5), "rounds down the division of two numbers")
    print(round_to_full_number(-3, 5), "rounds up the division of negative numbers")
    print(xor(3, 5), "is the xor of 3 and 5")
    print(return_rest_of_division(3, 5), "is the rest of division")
    print(normalize_hour(3), "is the current time plus 3 hours")
    print(round_function(42.5), "is the rounded value of 42.5")
    print(round_function(43.5), "is the rounded value of 43.5")