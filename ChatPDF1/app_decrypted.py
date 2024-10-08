import streamlit as st
from cryptography.fernet import Fernet

# Load the encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Load the encrypted code
with open('encrypted_app.py.enc', 'rb') as encrypted_file:
    encrypted_code = encrypted_file.read()

# Create a cipher suite
cipher_suite = Fernet(key)

# Decrypt the code
decrypted_code = cipher_suite.decrypt(encrypted_code).decode()

# Execute the decrypted code
exec(decrypted_code)
