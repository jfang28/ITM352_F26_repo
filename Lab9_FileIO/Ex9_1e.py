#Rewrite the below using the .readlines() method. 

with open("./names.txt", "r") as file:
    names = []
    lines = file.readlines()
    for line in lines:
        name = line.strip()
        if name:
            names.append(name)

    for name in names:
        print(name)
    print("Total names:", len(names))