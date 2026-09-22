from cryptography.fernet import Fernet


key = Fernet.generate_key()
cipher = Fernet(key)
message = input("Enter a message to encrypt: ")

# Fernet works with bytes, so encode the string before encryption.
encoded_message = message.encode("utf-8")
encrypted_message = cipher.encrypt(encoded_message)
decrypted_message = cipher.decrypt(encrypted_message)

# Decryption returns bytes, so decode them back into a readable string.
print(f"Encrypted message: {encrypted_message}")
print(f"Decrypted message: {decrypted_message.decode('utf-8')}")
