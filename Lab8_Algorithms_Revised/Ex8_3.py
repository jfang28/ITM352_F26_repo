import random

additional_requirements = [
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "R6",
]

remaining_requirements = additional_requirements.copy()

if len(remaining_requirements) < 2:
    raise ValueError("At least two additional requirements are needed.")

requirement_1 = random.choice(remaining_requirements)
remaining_requirements.remove(requirement_1)
requirement_2 = random.choice(remaining_requirements)

print("Assigned additional requirements:")
print(requirement_1)
print(requirement_2)