import mne
import matplotlib.pyplot as plt

# ============================================================
# CHB-MIT EEG FILE
# ============================================================

edf_path = r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0\chb01\chb01_03.edf"

print("Loading EEG file...")

raw = mne.io.read_raw_edf(
    edf_path,
    preload=True,
    verbose=False
)

# ============================================================
# EEG INFORMATION
# ============================================================

print("\n========== EEG INFORMATION ==========")

print("Number of channels:", len(raw.ch_names))
print("Sampling frequency:", raw.info["sfreq"], "Hz")
print("Number of samples:", raw.n_times)
print(
    "Recording duration:",
    round(raw.times[-1] / 60, 2),
    "minutes"
)

print("\nChannel names:")
print(raw.ch_names)

# ============================================================
# KNOWN SEIZURE INTERVAL
# ============================================================

seizure_start = 2996
seizure_end = 3036

plot_start = seizure_start - 10
plot_duration = (seizure_end - seizure_start) + 20

print("\n========== SEIZURE INFORMATION ==========")
print("Seizure start:", seizure_start, "seconds")
print("Seizure end:", seizure_end, "seconds")
print("Plot start:", plot_start, "seconds")
print("Plot duration:", plot_duration, "seconds")

# ============================================================
# PLOT EEG AROUND SEIZURE
# ============================================================

print("\nPlotting seizure interval...")

raw.plot(
    start=plot_start,
    duration=plot_duration,
    n_channels=10,
    scalings="auto",
    title="CHB-MIT EEG - Seizure in chb01_03",
    show=True
)

plt.show()