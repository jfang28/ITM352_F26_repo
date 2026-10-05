def celsius_to_fahrenheit(celsius):
    assert celsius >= -273.15, "Temperature cannot be below absolute zero (-273.15 C)"
    return celsius * 9 / 5 + 32

celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = celsius_to_fahrenheit(celsius)
print(f"{celsius} C is {fahrenheit} F")