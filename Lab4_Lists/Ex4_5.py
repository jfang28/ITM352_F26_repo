name = input("Enter your name: ")
print("Title case:", name.title())

url = input("Enter a URL: ")
host = url.split("://", 1)[-1].split("/", 1)[0]
host_parts = host.split(".")
domain_name = host_parts[-2]
tld = host_parts[-1]
print("Domain name:", domain_name)
print("TLD:", tld)

email = input("Enter an email address: ")
email_parts = email.split("@")
print("Username:", email_parts[0])
print("Domain:", email_parts[1])

at_index = email.index("@")
print("Username using index and slicing:", email[:at_index])
print("Domain using index and slicing:", email[at_index + 1:])

sentence = input("Enter a sentence: ")
words = sentence.split()
words.reverse()
reversed_sentence = " ".join(words)
print("Reversed sentence:", reversed_sentence)
