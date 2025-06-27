import numpy as np

# Dummy data: 128-dim face encodings like face_recognition generates
dummy_encodings = [
    np.random.rand(128),  # Face encoding 1
    np.random.rand(128)   # Face encoding 2
]

dummy_names = ['alice', 'bob']

# Save to .npy file
data = {
    'encodings': dummy_encodings,
    'names': dummy_names
}

np.save('database/encodings.npy', data)
print("Dummy encodings generated and saved.")

