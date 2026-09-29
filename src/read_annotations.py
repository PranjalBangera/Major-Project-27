from pathlib import Path

# ============================================================
# CHB-MIT SEIZURE ANNOTATION INSPECTOR
# ============================================================

annotation_file = Path(
    r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0"
    r"\chb01\chb01_03.edf.seizures"
)

print("Reading annotation file...")
print(annotation_file)

if not annotation_file.exists():
    print("\nERROR: Annotation file not found.")
    raise SystemExit(1)

# Read as raw binary
data = annotation_file.read_bytes()

print("\n========== FILE INFORMATION ==========")
print("File size:", len(data), "bytes")

print("\n========== FIRST 100 BYTES ==========")
print(data[:100])

print("\n========== HEX ==========")
print(data[:100].hex(" "))

print("\nAnnotation file successfully read as binary.")