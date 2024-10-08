from cryptography.fernet import Fernet

# Generate a key and write it to a file (save this securely)
key = Fernet.generate_key()
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

# Load the key
cipher_suite = Fernet(key)

# Read the content of the app.py file
with open('app.py', 'rb') as file:
    original_code = file.read()

# Encrypt the code
encrypted_code = cipher_suite.encrypt(original_code)

# Save the encrypted code to a file
with open('encrypted_app.py.enc', 'wb') as encrypted_file:
    encrypted_file.write(encrypted_code)

print("Encryption complete. Key and encrypted file saved.")
