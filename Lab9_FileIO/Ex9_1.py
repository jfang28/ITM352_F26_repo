#Write Python code that opens the file using the appropriate file mode and displays the data type returned from open(). Explain why this is more useful than directly working with the file (i.e. immediately read/write).

file = open("./names.txt", "r")
print(type(file))
