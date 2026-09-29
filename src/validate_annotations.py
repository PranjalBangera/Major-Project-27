from pathlib import Path
import json

DATASET_ROOT = Path(
    r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"
)

ANNOTATION_FILE = DATASET_ROOT / "seizure_annotations.json"

with open(ANNOTATION_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print("========================================")
print("ANNOTATION VALIDATION")
print("========================================")

print("Total records:", len(data))

records_with_seizures = 0
total_seizures = 0

for record in data:

    seizures = record.get("seizures", [])

    if len(seizures) > 0:
        records_with_seizures += 1
        total_seizures += len(seizures)

print("Records containing seizures:", records_with_seizures)
print("Total seizure events:", total_seizures)

print("\nFirst 10 seizure records:")

shown = 0

for record in data:

    if record.get("seizures"):

        print(
            f"{record['patient']} | "
            f"{record['file']} | "
            f"{record['seizures']}"
        )

        shown += 1

        if shown == 10:
            break

print("\nValidation completed.")