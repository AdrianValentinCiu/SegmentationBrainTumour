import json
import csv
import nibabel as nib
import numpy as np
import os

# Load dataset.json
with open("./dataset/dataset.json", "r") as f:
    data = json.load(f)

# Label ID to name mapping
label_mapping = {int(k): v for k, v in data["labels"].items()}

output_rows = []

for item in data["training"]:
    image_name = os.path.basename(item["image"])  # Just the filename
    label_path = os.path.join("dataset", item["label"].lstrip("./"))  # Correct full path

    try:
        # Load label volume
        img = nib.load(label_path)
        label_data = img.get_fdata()
        unique_labels = sorted(np.unique(label_data).astype(int))

        # Convert to readable names
        readable_labels = [label_mapping.get(lid, str(lid)) for lid in unique_labels]

        # Append result
        output_rows.append([image_name, ",".join(readable_labels)])
    except Exception as e:
        print(f"Error loading {label_path}: {e}")

# Write CSV
with open("brats_readable_labels.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["image_name", "labels"])
    writer.writerows(output_rows)
