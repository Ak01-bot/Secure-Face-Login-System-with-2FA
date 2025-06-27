# app/face_utils.py

from cryptography.fernet import Fernet
import numpy as np

# Key generation (save this key securely and don’t regenerate every time)
def generate_key():
    return Fernet.generate_key()

def load_key():
    with open("secret.key", "rb") as file:
        return file.read()

def save_key(key):
    with open("secret.key", "wb") as file:
        file.write(key)

# Encryption
def encrypt_encodings(encodings):
    f = Fernet(load_key())
    encrypted = f.encrypt(encodings.tobytes())
    with open("database/encodings_encrypted.bin", "wb") as file:
        file.write(encrypted)

# Decryption
def decrypt_encodings():
    f = Fernet(load_key())
    with open("database/encodings_encrypted.bin", "rb") as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    return np.frombuffer(decrypted).reshape(-1, 128)
