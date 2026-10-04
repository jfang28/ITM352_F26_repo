age = int(input("Enter your age: "))
day = input("Enter the day of the week: ").capitalize()
matinee = input("Is it a matinee showing? (yes/no): ").capitalize()

senior = True if(age >= 65) else False
is_tuesday = True if(day == "Tuesday") else False
is_matinee = True if(matinee == "Yes") else False

price = 14  # normal price

if is_matinee:
    if age >= 65:
        price = 5
    else:
        price = 8
elif senior >= 65:
    price = 8
elif is_tuesday:
    price = 10

print(f"${price}")