import os
import re
import json

ROOT = r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"

summary_events = []

# ---------------------------------------------------------
# Read every summary file
# ---------------------------------------------------------

for patient in [f"chb{i:02d}" for i in range(1, 25)]:

    summary_file = os.path.join(
        ROOT,
        patient,
        f"{patient}-summary.txt"
    )

    if not os.path.exists(summary_file):
        continue

    with open(summary_file, "r", errors="ignore") as f:
        lines = [line.strip() for line in f]

    current_file = None
    current_start = None

    for line in lines:

        # File name
        if line.startswith("File Name:"):
            current_file = line.split(":", 1)[1].strip()

        # Both formats:
        #
        # Seizure Start Time: 2996 seconds
        # Seizure 1 Start Time: 13688 seconds
        #
        match = re.match(
            r"Seizure(?:\s+\d+)?\s+Start Time:\s*([0-9.]+)",
            line
        )

        if match:
            current_start = float(match.group(1))

        match = re.match(
            r"Seizure(?:\s+\d+)?\s+End Time:\s*([0-9.]+)",
            line
        )

        if match and current_file is not None and current_start is not None:

            end = float(match.group(1))

            summary_events.append({
                "patient": patient,
                "file": current_file,
                "start": current_start,
                "end": end
            })

            current_start = None


# ---------------------------------------------------------
# Read WFDB JSON
# ---------------------------------------------------------

json_file = os.path.join(
    ROOT,
    "seizure_annotations_wfdb.json"
)

with open(json_file, "r") as f:
    wfdb_data = json.load(f)


wfdb_events = []

for record in wfdb_data:

    for seizure in record["seizures"]:

        wfdb_events.append({
            "patient": record["patient"],
            "file": record["file"],
            "start": seizure["start"],
            "end": seizure["end"]
        })


# ---------------------------------------------------------
# Compare
# ---------------------------------------------------------

print("======================================")
print("SUMMARY vs WFDB ANNOTATION COMPARISON")
print("======================================")

print(f"Summary events : {len(summary_events)}")
print(f"WFDB events    : {len(wfdb_events)}")


missing = []

for s in summary_events:

    found = False

    for w in wfdb_events:

        if (
            s["patient"] == w["patient"]
            and s["file"] == w["file"]
            and abs(s["start"] - w["start"]) < 0.01
            and abs(s["end"] - w["end"]) < 0.01
        ):
            found = True
            break

    if not found:
        missing.append(s)


print("\nMissing from WFDB annotations:")
print("--------------------------------")

for event in missing:
    print(
        f"{event['patient']} | "
        f"{event['file']} | "
        f"{event['start']} -> {event['end']} sec"
    )

print("\n======================================")
print(f"Missing events: {len(missing)}")
print("======================================")