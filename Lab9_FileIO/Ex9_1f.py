#Now add your own name to the end of the file and print the entire contents of the file.
with open("./names.txt", "a") as file:
    file.write("\nJordan Fang\n")

with open("./names.txt", "r") as file:
    print(file.read())