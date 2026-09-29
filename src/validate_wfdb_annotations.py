import json
import os

ROOT = r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"

json_file = os.path.join(
    ROOT,
    "seizure_annotations_wfdb.json"
)

with open(json_file, "r") as f:
    data = json.load(f)

print("================================")
print("WFDB ANNOTATION VALIDATION")
print("================================")

print(f"Total records: {len(data)}")

records_with_seizures = [
    x for x in data if len(x["seizures"]) > 0
]

total_events = sum(
    len(x["seizures"])
    for x in data
)

print(f"Records containing seizures: {len(records_with_seizures)}")
print(f"Total seizure events: {total_events}")

print("\nFirst 10 seizure records:")
print("--------------------------------")

for record in records_with_seizures[:10]:

    print(
        f"{record['patient']} | "
        f"{record['file']} | "
        f"{record['seizures']}"
    )

print("\nChecking annotation times...")

errors = 0

for record in data:

    for seizure in record["seizures"]:

        start = seizure["start"]
        end = seizure["end"]

        if start < 0:
            print(
                f"ERROR: Negative start time: "
                f"{record['file']}"
            )
            errors += 1

        if end <= start:
            print(
                f"ERROR: Invalid interval: "
                f"{record['file']} "
                f"{start} -> {end}"
            )
            errors += 1

        if seizure["end_sample"] <= seizure["start_sample"]:
            print(
                f"ERROR: Invalid samples: "
                f"{record['file']}"
            )
            errors += 1

print("\n================================")

if errors == 0:
    print("VALIDATION PASSED")
else:
    print(f"VALIDATION FAILED: {errors} errors")

print("================================")