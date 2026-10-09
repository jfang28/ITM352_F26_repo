items = ("hello", 10, "goodbye", 3, "goodnight", 5)

user_input = input("Enter a value to append: ")

try:
    items.append(user_input)
except AttributeError:
    items_list = list(items)
    items_list.append(user_input)
    items = tuple(items_list)

print(items)