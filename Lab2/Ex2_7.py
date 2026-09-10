'''
Write Python code that uses the input built-in function to ask the user to enter a temperature in the Fahrenheit temperature scale. The input function always returns a string value, so use the float built-in function to convert the value entered to a float data type and determine the equivalent temperature in the Celsius temperature scale (use the conversion factor °C = (°F – 32) × (5/9)). Print a message to the user stating the temperature in Fahrenheit that they entered and the equivalent temperature in Celsius. You can verify that your code executes properly by entering in 32°F (equivalent is 0°C) and 212°F (equivalent is 100°C).
'''

def fahrenheit_to_celsius(temperature_fahrenheit):
    return (temperature_fahrenheit - 32) * (5 / 9)

# Test the function with known benchmark values.
assert fahrenheit_to_celsius(32) == 0
assert fahrenheit_to_celsius(212) == 100

# Prompt the user and print the converted temperature.
temperature_fahrenheit = float(input("Please enter a temperature in Fahrenheit: "))
temperature_celsius = fahrenheit_to_celsius(temperature_fahrenheit)
print(f"You entered {temperature_fahrenheit}°F, which is equivalent to {temperature_celsius}°C.")
