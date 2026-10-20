"The GCD (greatest common divisor) of two numbers is the largest number that divides both evenly. For example, GCD(48, 18) = 6.  Create an algorithm that computes this number."

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

number1 = int(input("Enter a number: "))
number2 = int(input("Enter another number: "))
print("The GCD of", number1, "and", number2, "is", gcd(number1, number2))