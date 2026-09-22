def midpoint(first_number, second_number):
    """Return the value halfway between two numbers."""
    return (first_number + second_number) / 2


def squareroot(number):
    """Return the square root of a number."""
    return number ** 0.5


def exponent(base, power):
    """Return the base raised to the given power."""
    return base ** power


def max(first_number, second_number):
    """Return the larger of two numbers."""
    return first_number if first_number > second_number else second_number


def min(first_number, second_number):
    """Return the smaller of two numbers."""
    return first_number if first_number < second_number else second_number


def apply_function(first_number, second_number, function):
    """Describe the result of applying a two-number function."""
    return (f"The function {function.__name__} {first_number},{second_number} = "
            f"{function(first_number, second_number)}")
