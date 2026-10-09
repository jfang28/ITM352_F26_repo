items = ("hello", 10, "goodbye", 3, "goodnight", 5)

user_input = input("Enter a value to append: ")

try:
    items.append(user_input)
except AttributeError:
    items = (*items, user_input)

print(items)