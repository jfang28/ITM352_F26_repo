#Rewrite the below using the .readline() method.

with open("./names.txt", "r") as file:
    names = []
    line = file.readline()
    while line:
        name = line.strip()
        if name:
            names.append(name)
        line = file.readline()

    for name in names:
        print(name)
    print("Total names:", len(names))
