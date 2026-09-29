import os
import re
import numpy as np
import mne

# ============================================================
# PATHS
# ============================================================

BASE_DIR = r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"

OUTPUT_DIR = r"D:\Majorproject27\data\processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Test only these 3 recordings for now
RECORDS = [
    "chb01/chb01_03.edf",
    "chb01/chb01_04.edf",
    "chb01/chb01_15.edf",
]

WINDOW_SECONDS = 5
EXPECTED_FS = 256


# ============================================================
# FIND SEIZURE TIMES FROM SUMMARY FILE
# ============================================================

def get_seizure_intervals(summary_file, edf_name):

    with open(summary_file, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Find the section belonging to this EDF file
    pattern = rf"File Name:\s*{re.escape(edf_name)}(.*?)(?=\nFile Name:|\Z)"

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if not match:
        raise ValueError(f"Could not find {edf_name} in summary file.")

    section = match.group(1)

    starts = re.findall(
        r"Seizure Start Time:\s*(\d+)",
        section,
        re.IGNORECASE
    )

    ends = re.findall(
        r"Seizure End Time:\s*(\d+)",
        section,
        re.IGNORECASE
    )

    intervals = []

    for start, end in zip(starts, ends):
        intervals.append((int(start), int(end)))

    return intervals


# ============================================================
# EXTRACT 5-SECOND WINDOWS
# ============================================================

def extract_windows(raw, intervals):

    fs = int(raw.info["sfreq"])

    if fs != EXPECTED_FS:
        raise ValueError(
            f"Unexpected sampling frequency: {fs} Hz"
        )

    n_channels = len(raw.ch_names)

    seizure_windows = []
    non_seizure_windows = []

    total_seconds = raw.times[-1]

    # --------------------------------------------------------
    # Seizure windows
    # --------------------------------------------------------

    for start_sec, end_sec in intervals:

        current = start_sec

        while current + WINDOW_SECONDS <= end_sec:

            start_sample = int(current * fs)
            end_sample = int((current + WINDOW_SECONDS) * fs)

            data = raw.get_data(
                start=start_sample,
                stop=end_sample
            )

            seizure_windows.append(data)

            current += WINDOW_SECONDS

    # --------------------------------------------------------
    # Non-seizure windows
    # --------------------------------------------------------
    # For this initial test, take windows from the beginning
    # of the recording and make sure they don't overlap seizure.
    # --------------------------------------------------------

    current = 0

    while current + WINDOW_SECONDS <= total_seconds:

        candidate_start = current
        candidate_end = current + WINDOW_SECONDS

        overlaps_seizure = False

        for seizure_start, seizure_end in intervals:

            if (
                candidate_start < seizure_end
                and candidate_end > seizure_start
            ):
                overlaps_seizure = True
                break

        if not overlaps_seizure:

            start_sample = int(candidate_start * fs)
            end_sample = int(candidate_end * fs)

            data = raw.get_data(
                start=start_sample,
                stop=end_sample
            )

            non_seizure_windows.append(data)

            # Keep equal number for this demo
            if len(non_seizure_windows) >= len(seizure_windows):
                break

        current += WINDOW_SECONDS

    # Convert lists to NumPy arrays

    if seizure_windows:
        seizure_windows = np.stack(seizure_windows)
    else:
        seizure_windows = np.empty(
            (0, n_channels, WINDOW_SECONDS * fs)
        )

    if non_seizure_windows:
        non_seizure_windows = np.stack(non_seizure_windows)
    else:
        non_seizure_windows = np.empty(
            (0, n_channels, WINDOW_SECONDS * fs)
        )

    return seizure_windows, non_seizure_windows


# ============================================================
# PROCESS RECORDINGS
# ============================================================

all_X = []
all_y = []

for record in RECORDS:

    print("\n" + "=" * 60)
    print(f"Processing: {record}")

    subject = record.split("/")[0]
    edf_name = os.path.basename(record)

    edf_path = os.path.join(BASE_DIR, record)

    summary_path = os.path.join(
        BASE_DIR,
        subject,
        f"{subject}-summary.txt"
    )

    print(f"EDF:     {edf_path}")
    print(f"Summary: {summary_path}")

    # --------------------------------------------------------
    # Get seizure annotations
    # --------------------------------------------------------

    intervals = get_seizure_intervals(
        summary_path,
        edf_name
    )

    print(f"Seizure intervals: {intervals}")

    # --------------------------------------------------------
    # Load EDF
    # --------------------------------------------------------

    raw = mne.io.read_raw_edf(
        edf_path,
        preload=False,
        verbose=False
    )

    print(f"Sampling frequency: {raw.info['sfreq']} Hz")
    print(f"Channels: {len(raw.ch_names)}")
    print(f"Duration: {raw.times[-1]:.2f} seconds")

    # --------------------------------------------------------
    # Extract windows
    # --------------------------------------------------------

    X_seizure, X_non_seizure = extract_windows(
        raw,
        intervals
    )

    print(f"Seizure windows:     {len(X_seizure)}")
    print(f"Non-seizure windows: {len(X_non_seizure)}")

    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

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

    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")

    # --------------------------------------------------------
    # Save individual recording
    # --------------------------------------------------------

    safe_name = edf_name.replace(".edf", "")

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{safe_name}_dataset.npz"
    )

    np.savez_compressed(
        output_file,
        X=X,
        y=y
    )

    print(f"Saved: {output_file}")

    all_X.append(X)
    all_y.append(y)


# ============================================================
# COMBINE ALL 3 RECORDINGS
# ============================================================

X_all = np.concatenate(all_X, axis=0)
y_all = np.concatenate(all_y, axis=0)

combined_file = os.path.join(
    OUTPUT_DIR,
    "chb01_demo_dataset.npz"
)

np.savez_compressed(
    combined_file,
    X=X_all,
    y=y_all
)

# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 60)
print("DATASET CREATION COMPLETE")
print("=" * 60)

print(f"Final X shape: {X_all.shape}")
print(f"Final y shape: {y_all.shape}")

print(f"Seizure samples:     {np.sum(y_all == 1)}")
print(f"Non-seizure samples: {np.sum(y_all == 0)}")

print(f"\nSaved combined dataset:")
print(combined_file)