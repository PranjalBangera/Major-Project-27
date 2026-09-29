import numpy as np
import matplotlib.pyplot as plt

# Load dataset
dataset_path = r"D:\Majorproject27\data\processed\chb01_demo_dataset.npz"

data = np.load(dataset_path)

X = data["X"]
y = data["y"]

print("X shape:", X.shape)
print("y shape:", y.shape)

# Select first seizure sample
sample_index = np.where(y == 0)[0][0]

sample = X[sample_index]

print("Selected sample:", sample_index)
print("Label:", y[sample_index])
print("Sample shape:", sample.shape)

# Plot first EEG channel
plt.figure(figsize=(12, 5))

plt.plot(sample[0])

plt.title("Saved EEG Window - Non-Seizure Sample")
plt.xlabel("Sample")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()