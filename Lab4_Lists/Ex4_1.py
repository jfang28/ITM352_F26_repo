first_name = input("Enter your first name: ")
middle_initial = input("Enter your middle initial: ")
last_name = input("Enter your last name: ")

# Using the + concatenation operator
full_name_plus = first_name + " " + middle_initial + " " + last_name
print(full_name_plus)

# Using an f-string
full_name_fstring = f"{first_name} {middle_initial} {last_name}"
print(full_name_fstring)

# Using the % operator
full_name_percent = "%s %s %s" % (first_name, middle_initial, last_name)
print(full_name_percent)

# Using the format() method
full_name_format = "{} {} {}".format(
    first_name, middle_initial, last_name
)
print(full_name_format)

# Using the join() method
name_parts = [first_name, middle_initial, last_name]
full_name_join = " ".join(name_parts)
print(full_name_join)

# Using format() with the list unpacked as arguments
full_name_unpack = "{} {} {}".format(*name_parts)
print(full_name_unpack)