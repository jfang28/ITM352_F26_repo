'''
Write Python code that uses the input built-in function to ask the user to enter a decimal formatted number between 1 and 100. Square the number that the user entered using the exponentiation operator. Print a message to the user stating the value that they entered and the square of the value that they entered.
'''
# Ask the user for a decimal number and convert the text input into a float.
number = float(input("Please enter a decimal formatted number between 1 and 100: "))

# Square the number using the exponentiation operator.
square = number ** 2

# Round the displayed values before showing them to the user.
print(f"You entered {round(number, 2)}, and its square is {round(square, 2)}.")
