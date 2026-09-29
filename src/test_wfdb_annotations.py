import wfdb

edf_path = r"D:\Majorproject27\CHBMIT\physionet.org\files\chbmit\1.0.0\chb01\chb01_03.edf"

print("Reading annotation file...")

ann = wfdb.rdann(
    edf_path,
    extension="seizures"
)

print("\n===== WFDB ANNOTATION RESULT =====")

print("Number of annotations:", len(ann.sample))

print("\nAnnotation samples:")
print(ann.sample)

print("\nAnnotation symbols:")
print(ann.symbol)

print("\nAnnotation auxiliary notes:")
print(ann.aux_note)

print("\nSampling frequency:", ann.fs)

print("\n===== CONVERTED TO SECONDS =====")

for sample, symbol in zip(ann.sample, ann.symbol):
    time_sec = sample / ann.fs
    print(f"Sample: {sample:8d} | Time: {time_sec:8.2f} sec | Symbol: {symbol}")