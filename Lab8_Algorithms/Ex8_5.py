"Create an algorithm that determines whether a string entered by the user is a palindrome (that is, the string is the same when read forwards or backwards)."

def is_palindrome(s):
    return s == s[::-1]

user_input = input("Enter a string: ")
if is_palindrome(user_input):
    print(user_input, "is a palindrome.")
else:
    print(user_input, "is not a palindrome.")