def isLeapYear(year):
    if year % 400 == 0:
        return "Leap year"
    elif year % 100 == 0:
        return "Not a leap year"
    elif year % 4 == 0:
        return "Leap year"
    else:
        return "Not a leap year"

year = int(input("Enter a year: "))
print(f"{year}: {isLeapYear(year)}")