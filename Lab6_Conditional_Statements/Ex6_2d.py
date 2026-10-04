test_lists = [
	["apple", 42, 3.14],
	["apple", 42, 3.14, True, "banana"],
	["apple", 42, 3.14, True, "banana", 7, "orange", False, 2.5, "grape"],
	["apple", 42, 3.14, True, "banana", 7, "orange", False, 2.5, "grape", "pear"],
]

def check_list_size(values, minimum=5, maximum=10):
    size = len(values)
    print(f"List has {size} elements.")

    if size < minimum:
        print(f"The list has fewer than {minimum} elements.")
    elif size <= maximum:
        print(f"The list has between {minimum} and {maximum} elements.")
    else:
        print(f"The list has more than {maximum} elements.")

for values in test_lists:
    check_list_size(values)