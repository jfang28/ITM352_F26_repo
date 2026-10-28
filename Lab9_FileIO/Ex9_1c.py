# Using the .read() method, read the names from names.txt and print them
# along with the count of nonblank names.
with open("./names.txt", "r") as file:
    names = [name.strip() for name in file.read().split("\n") if name.strip()]
    for name in names:
        print(name)
    print("Total names:", len(names))