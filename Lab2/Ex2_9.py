t = float(input("Enter the temperature: "))
conv = input("Enter the conversion type (C for Celsius to Fahrenheit, F for Fahrenheit to Celsius): ")
tmp = 9 / 5 * t + 32 if conv == 'C' else (t - 32) * 5 / 9
print(f"The converted temperature is: {tmp}")
