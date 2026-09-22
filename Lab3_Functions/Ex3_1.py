import cryptography

print("cryptography imported successfully")
print(f"Version: {cryptography.__version__}")

from cryptography.fernet import Fernet


key = Fernet.generate_key()
cipher = Fernet(key)
message = input("Enter a string to encrypt: ")

encrypted_message = cipher.encrypt(message.encode("utf-8"))
decrypted_message = cipher.decrypt(encrypted_message).decode("utf-8")

print(f"Encrypted string: {encrypted_message}")
print(f"Decrypted string: {decrypted_message}")