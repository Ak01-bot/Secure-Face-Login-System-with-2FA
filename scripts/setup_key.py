import sys
import os

# Add the parent directory (project root) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.face_utils import generate_key, save_key

# Generate and save the encryption key
save_key(generate_key())
print("Encryption key generated and saved as secret.key")
