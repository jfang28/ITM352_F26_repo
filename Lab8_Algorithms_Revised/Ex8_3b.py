def assign_requirements(student_id):
    "Return two different requirement numbers, from 1 through 7."
    digits = [int(digit) for digit in student_id]
    digit_sum = sum(digits)

    nonzero_product = 1
    for digit in digits:
        if digit != 0:
            nonzero_product *= digit

    first_num = digit_sum % 7 + 1
    second_num = nonzero_product % 7 + 1

    while first_num == second_num:
        second_num = second_num % 7 + 1

    return first_num, second_num


student_id = input("Enter your student ID: ").strip()

while not student_id or not student_id.isdigit() or len(student_id) != 8:
    if not student_id:
        print("Student ID must not be empty.")
    elif not student_id.isdigit():
        print("Student ID must contain digits only.")
    elif len(student_id) != 8:
        print("Student ID must be 8 digits long.")
    student_id = input("Enter your student ID: ").strip()

first_num, second_num = assign_requirements(student_id)
print("Your two additional requirements are:")
print(f"R{first_num} and R{second_num}")
