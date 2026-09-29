import mne
import numpy as np

# ============================================================
# CHB-MIT EEG file
# ============================================================

edf_path = r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0\chb01\chb01_03.edf"

# Seizure interval obtained from chb01-summary.txt
SEIZURE_START = 2996
SEIZURE_END = 3036

# Window length
WINDOW_SECONDS = 5

print("Loading EEG file...")

raw = mne.io.read_raw_edf(
    edf_path,
    preload=False,
    verbose=False
)

# Keep EEG channels only
raw.pick_types(eeg=True)

sfreq = raw.info["sfreq"]

print("\n========== EEG DATA ==========")
print("Sampling frequency:", sfreq, "Hz")
print("Number of EEG channels:", len(raw.ch_names))
print("Window size:", WINDOW_SECONDS, "seconds")
print("Samples per window:", int(WINDOW_SECONDS * sfreq))

# ============================================================
# Function to extract windows
# ============================================================

def extract_windows(raw, start_time, end_time, label):

    windows = []

    current_time = start_time

    while current_time + WINDOW_SECONDS <= end_time:

        segment = raw.copy().crop(
            tmin=current_time,
            tmax=current_time + WINDOW_SECONDS,
            include_tmax=False
        )

        data = segment.get_data()

        windows.append(data)

        print(
            f"Window: {current_time:.0f}-{current_time + WINDOW_SECONDS:.0f} sec"
            f" | Shape: {data.shape}"
            f" | Label: {label}"
        )

        current_time += WINDOW_SECONDS

    return windows


# ============================================================
# Extract seizure windows
# ============================================================

print("\n========== SEIZURE WINDOWS ==========")

seizure_windows = extract_windows(
    raw,
    SEIZURE_START,
    SEIZURE_END,
    label=1
)

# ============================================================
# Extract clearly non-seizure windows
# ============================================================

print("\n========== NON-SEIZURE WINDOWS ==========")

# Far away from the known seizure interval
NON_SEIZURE_START = 1000
NON_SEIZURE_END = 1040

non_seizure_windows = extract_windows(
    raw,
    NON_SEIZURE_START,
    NON_SEIZURE_END,
    label=0
)

# ============================================================
# Convert to NumPy arrays
# ============================================================

X_seizure = np.array(seizure_windows)
X_non_seizure = np.array(non_seizure_windows)

print("\n========== FINAL DATASET CHECK ==========")

print("Seizure dataset shape:", X_seizure.shape)
print("Non-seizure dataset shape:", X_non_seizure.shape)

print("\nExpected format:")
print("(number_of_windows, channels, samples)")
# ============================================================
# Combine seizure and non-seizure data
# ============================================================

X = np.concatenate(
    [X_seizure, X_non_seizure],
    axis=0
)

y = np.concatenate(
    [
        np.ones(len(X_seizure), dtype=np.int64),
        np.zeros(len(X_non_seizure), dtype=np.int64)
    ]
)

print("\n========== COMBINED DATASET ==========")

print("X shape:", X.shape)
print("y shape:", y.shape)

print("Seizure samples:", np.sum(y == 1))
print("Non-seizure samples:", np.sum(y == 0))
# ============================================================
# Save processed demo dataset
# ============================================================

import os

output_dir = r"D:\Majorproject27\data\processed"

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    "chb01_03_demo.npz"
)

np.savez_compressed(
    output_file,
    X=X,
    y=y
)

print("\n========== DATASET SAVED ==========")
print("Saved to:", output_file)