values = ["apple", 42, 3.14, True, "banana", 7, "orange", False, 2.5, "grape", "pear"]
test_lists = [values[:3], values[:5], values[:10], values]

for test_list in test_lists:
	print(f"List has {len(test_list)} elements.")

	if len(test_list) < 5:
		print("The list has fewer than 5 elements.")
	elif len(test_list) <= 10:
		print("The list has between 5 and 10 elements.")
	else:
		print("The list has more than 10 elements.")

