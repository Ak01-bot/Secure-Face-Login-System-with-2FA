import numpy as np

data = np.load('database/encodings.npy', allow_pickle=True).item()

print("Encodings count:", len(data['encodings']))
print("Names:", data['names'])

# Check the shape of one encoding vector
if data['encodings']:
    print("One encoding shape:", data['encodings'][0].shape)
