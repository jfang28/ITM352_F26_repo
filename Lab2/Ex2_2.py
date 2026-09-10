'''
Write Python code that uses the input built-in function to ask the user to enter the year they were born as a four-digit number. Print a message to the user stating the value that they entered and their calculated age. Make sure you correctly handle the data types in the expressions to get the expected results.
'''
birth_year = int(input("Enter the year you were born as a four-digit number: "))

current_year = 2026
age = current_year - birth_year

print("You entered:", birth_year)
print("Your calculated age is:", age)