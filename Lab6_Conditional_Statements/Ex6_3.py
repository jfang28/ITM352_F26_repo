age = int(input("Enter your age: "))
weekday = input("Enter the day of the week: ").strip().capitalize()
matinee = input("Is it a matinee showing? (yes/no): ").strip().lower() == "yes"

senior = age >= 65
is_tuesday = weekday.lower() == "tuesday"

price = 14  # normal price

if matinee:
    if senior:
        price = 5
    else:
        price = 8
elif senior:
    price = 8
elif is_tuesday:
    price = 10

print(f"${price}")