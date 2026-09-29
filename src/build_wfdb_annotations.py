import os
import json
import wfdb

ROOT = r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"

records_file = os.path.join(ROOT, "RECORDS-WITH-SEIZURES")
output_file = os.path.join(ROOT, "seizure_annotations_wfdb.json")

annotations = []

with open(records_file, "r") as f:
    records = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

print(f"Records to process: {len(records)}")

for i, record in enumerate(records, start=1):

    record_path = os.path.join(ROOT, record)

    try:
        ann = wfdb.rdann(
    record_path,
    extension="seizures"
)
        

        seizures = []

        start_sample = None

        for sample, symbol in zip(ann.sample, ann.symbol):

            if symbol == "[":
                start_sample = int(sample)

            elif symbol == "]" and start_sample is not None:

                start_sec = start_sample / ann.fs
                end_sec = sample / ann.fs

                seizures.append({
                    "start": start_sec,
                    "end": end_sec,
                    "duration": end_sec - start_sec,
                    "start_sample": start_sample,
                    "end_sample": int(sample)
                })

                start_sample = None

        patient = record.split("/")[0]
        filename = record.split("/")[-1]

        annotations.append({
            "patient": patient,
            "file": filename,
            "path": record,
            "sampling_frequency": ann.fs,
            "seizures": seizures
        })

        print(
            f"[{i}/{len(records)}] "
            f"{record} -> {len(seizures)} seizure(s)"
        )

    except Exception as e:

        print(f"ERROR: {record}")
        print(e)


with open(output_file, "w") as f:
    json.dump(annotations, f, indent=4)

print("\n================================")
print("ANNOTATION EXTRACTION COMPLETE")
print("================================")

print(f"Total records: {len(annotations)}")

records_with_seizures = sum(
    1 for x in annotations if x["seizures"]
)

total_events = sum(
    len(x["seizures"])
    for x in annotations
)

print(f"Records containing seizures: {records_with_seizures}")
print(f"Total seizure events: {total_events}")

print(f"\nSaved to:")
print(output_file)