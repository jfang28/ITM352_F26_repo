'''
Create a function—call it midpoint —that takes two numbers as input and returns the value halfway between them. 
Explain the benefit of creating this function:
Explain if the function is named appropriately:
'''
def midpoint(first_number, second_number):
    """Return the value halfway between two numbers."""
    return (first_number + second_number) / 2


first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))
print(f"The midpoint is {midpoint(first_number, second_number)}")
