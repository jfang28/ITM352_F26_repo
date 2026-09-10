'''
Write Python code that uses the input built-in function to ask the user to enter a sentence of their choosing. Use the len built-in function to determine how many characters were in the string entered and report this information back to the user.
'''
sentence = input("Please enter a sentence of your choosing: ")
char_count = len(sentence)
print(f"The sentence you entered has {char_count} characters.")

last_index = char_count - 1
last_char = sentence[last_index]
print(f"The last character is: {last_char}")
