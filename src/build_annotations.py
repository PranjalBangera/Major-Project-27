from pathlib import Path
import re
import json

# ============================================================
# CHB-MIT DATASET ROOT
# ============================================================

DATASET_ROOT = Path(
    r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"
)

OUTPUT_FILE = DATASET_ROOT / "seizure_annotations.json"


def parse_summary_file(summary_file):
    records = []

    current_record = None

    with open(summary_file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if line.startswith("File Name:"):

                filename = line.split(":", 1)[1].strip()

                current_record = {
                    "file": filename,
                    "seizures": []
                }

                records.append(current_record)

            elif line.startswith("Number of Seizures in File:"):

                count = int(
                    line.split(":", 1)[1].strip()
                )

                current_record["number_of_seizures"] = count

            elif line.startswith("Seizure Start Time:"):

                start = float(
                    re.search(
                        r"([\d.]+)",
                        line
                    ).group(1)
                )

                current_record["seizures"].append({
                    "start": start,
                    "end": None
                })

            elif line.startswith("Seizure End Time:"):

                end = float(
                    re.search(
                        r"([\d.]+)",
                        line
                    ).group(1)
                )

                current_record["seizures"][-1]["end"] = end

    return records


# ============================================================
# SCAN ALL PATIENT FOLDERS
# ============================================================

all_records = []

patient_dirs = sorted(
    DATASET_ROOT.glob("chb*")
)

print("Scanning CHB-MIT dataset...")
print("Dataset root:", DATASET_ROOT)

for patient_dir in patient_dirs:

    if not patient_dir.is_dir():
        continue

    summary_files = list(
        patient_dir.glob("*-summary.txt")
    )

    if not summary_files:
        continue

    summary_file = summary_files[0]

    print(
        f"Processing {patient_dir.name}..."
    )

    records = parse_summary_file(
        summary_file
    )

    for record in records:

        if record.get("number_of_seizures", 0) > 0:

            record["patient"] = patient_dir.name

            all_records.append(record)


# ============================================================
# SAVE JSON
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_records,
        f,
        indent=4
    )


# ============================================================
# SUMMARY
# ============================================================

total_files = len(all_records)

total_seizures = sum(
    len(record["seizures"])
    for record in all_records
)

print("\n========================================")
print("ANNOTATION BUILD COMPLETE")
print("========================================")

print("Files containing seizures:", total_files)
print("Total seizure events:", total_seizures)

print("\nSaved to:")
print(OUTPUT_FILE)