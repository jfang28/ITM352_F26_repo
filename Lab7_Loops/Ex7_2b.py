even_numbers = [2]
number = 3
while even_numbers[-1] < 50:
    if number % 2 == 0:
        even_numbers.append(number)
    number += 1
print(even_numbers)
