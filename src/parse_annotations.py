from pathlib import Path
import re

# ============================================================
# CHB-MIT SUMMARY FILE PARSER
# ============================================================

DATASET_ROOT = Path(
    r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"
)

SUMMARY_FILE = DATASET_ROOT / "chb01" / "chb01-summary.txt"


def parse_summary_file(summary_file):
    """
    Parse CHB-MIT patient summary file.

    Returns:
        list of dictionaries containing:
        - EDF filename
        - seizure count
        - seizure start/end times
    """

    results = []

    current_file = None
    current_record = None

    with open(summary_file, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            # ------------------------------------------------
            # EDF filename
            # ------------------------------------------------

            if line.startswith("File Name:"):

                filename = line.split(":", 1)[1].strip()

                current_file = filename

                current_record = {
                    "file": filename,
                    "seizures": []
                }

                results.append(current_record)

            # ------------------------------------------------
            # Number of seizures
            # ------------------------------------------------

            elif line.startswith("Number of Seizures in File:"):

                count = int(
                    line.split(":", 1)[1].strip()
                )

                current_record["number_of_seizures"] = count

            # ------------------------------------------------
            # Seizure start
            # ------------------------------------------------

            elif line.startswith("Seizure Start Time:"):

                start = float(
                    re.search(
                        r"([\d.]+)",
                        line
                    ).group(1)
                )

                current_record["seizures"].append(
                    {
                        "start": start,
                        "end": None
                    }
                )

            # ------------------------------------------------
            # Seizure end
            # ------------------------------------------------

            elif line.startswith("Seizure End Time:"):

                end = float(
                    re.search(
                        r"([\d.]+)",
                        line
                    ).group(1)
                )

                current_record["seizures"][-1]["end"] = end

    return results


# ============================================================
# RUN PARSER
# ============================================================

print("Reading:", SUMMARY_FILE)

records = parse_summary_file(SUMMARY_FILE)

print("\n========== PARSED SEIZURE INFORMATION ==========")

for record in records:

    if record.get("number_of_seizures", 0) > 0:

        print("\nEDF:", record["file"])

        for i, seizure in enumerate(
            record["seizures"],
            start=1
        ):

            print(
                f"Seizure {i}: "
                f"{seizure['start']} s → "
                f"{seizure['end']} s"
            )

print("\nParsing completed successfully.")