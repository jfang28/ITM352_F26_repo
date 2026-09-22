def c_to_f(celsius):
    return (celsius * 9 / 5) + 32


def f_to_c(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def c_to_k(celsius):
    return celsius + 273.15


def k_to_c(kelvin):
    return kelvin - 273.15


def f_to_k(fahrenheit):
    return c_to_k(f_to_c(fahrenheit))


def k_to_f(kelvin):
    return c_to_f(k_to_c(kelvin))


def convert_temperature(value, conversion_func):
    """Apply a passed-in conversion function to a temperature value."""
    return conversion_func(value)


if __name__ == "__main__":
    print(f"0 C = {convert_temperature(0, c_to_f):.2f} F")
    print(f"32 F = {convert_temperature(32, f_to_c):.2f} C")
    print(f"0 C = {convert_temperature(0, c_to_k):.2f} K")
    print(f"273.15 K = {convert_temperature(273.15, k_to_c):.2f} C")
    print(f"212 F = {convert_temperature(212, f_to_k):.2f} K")
    print(f"273.15 K = {convert_temperature(273.15, k_to_f):.2f} F")
