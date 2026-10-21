import random

def assign_pair(student_id, requirement_count):
    """Return the pair selected by the shuffled-pair-list algorithm."""
    if requirement_count < 2:
        raise ValueError("There must be at least two requirements.")
    if not student_id.isdigit() or len(student_id) != 8:
        raise ValueError("Student ID must be exactly 8 digits.")

    pairs = []
    for first in range(1, requirement_count):
        for second in range(first + 1, requirement_count + 1):
            pairs.append((first, second))
    random.shuffle(pairs)
    pair_index = (int(student_id) - 10_000_000) % len(pairs)
    return pairs[pair_index]


requirement_count = input("How many requirements are there? ").strip()
while not requirement_count.isdigit() or int(requirement_count) < 2:
    print("Enter a whole number of at least 2.")
    requirement_count = input("How many requirements are there? ").strip()

student_id = input("Enter your 8-digit student ID: ").strip()
while not student_id.isdigit() or len(student_id) != 8:
    print("Student ID must be exactly 8 digits.")
    student_id = input("Enter your 8-digit student ID: ").strip()

first_requirement, second_requirement = assign_pair(
    student_id, int(requirement_count)
)
print("Your two additional requirements are:")
print(f"R{first_requirement} and R{second_requirement}")