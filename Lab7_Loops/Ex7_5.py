celebrities_tuple = ("Zendaya", "Timothée Chalamet", "Billie Eilish", "Dwayne Johnson", "Rihanna")
ages_tuple = (30, 30, 24, 54, 38)

celebrities_list = []
ages_list = []

for celebrity in celebrities_tuple:
    celebrities_list.append(celebrity)

for age in ages_tuple:
    ages_list.append(age)

celebrities_and_ages = {
    "celebrities": celebrities_list,
    "ages": ages_list,
}

print(celebrities_and_ages)