import HandyMath


first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))

print(f"The midpoint is {HandyMath.midpoint(first_number, second_number)}")
print(f"The square root of the square of the first number is "
      f"{HandyMath.squareroot(first_number ** 2)}")
print(f"The first number raised to the second number is "
      f"{HandyMath.exponent(first_number, second_number)}")
print(f"The maximum is {HandyMath.max(first_number, second_number)}")
print(f"The minimum is {HandyMath.min(first_number, second_number)}")