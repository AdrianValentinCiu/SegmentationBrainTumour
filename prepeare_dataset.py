import os
import json
import nibabel as nib


def decompress_with_nibabel(src_path, dst_path):
    """
    Load compressed or uncompressed NIfTI using nibabel and save as uncompressed .nii
    """
    try:
        img = nib.load(src_path)
        nib.save(img, dst_path)
        print(f"Saved: {dst_path}")
    except Exception as e:
        print(f"Failed to decompress {src_path}: {e}")


def unzip_nii_gz_folder(src_folder, dst_folder):
    """
    Recursively decompress all .nii.gz files in src_folder to .nii in dst_folder
    while preserving folder structure.
    """
    os.makedirs(dst_folder, exist_ok=True)
    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith('.nii.gz'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_folder)
                out_path = os.path.join(dst_folder, rel_path).replace('.nii.gz', '.nii')
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                decompress_with_nibabel(src_path, out_path)


def update_dataset_json(original_json_path, updated_json_path, original_base, unzipped_base):
    """
    Modify dataset.json paths to point to the uncompressed files.
    """
    with open(original_json_path) as f:
        dataset = json.load(f)

    def fix_path(p):
        rel = os.path.relpath(p, original_base).replace(".nii.gz", ".nii")
        return os.path.normpath(os.path.join(unzipped_base, rel))

    for entry in dataset['training']:
        entry['image'] = fix_path(entry['image'])
        entry['label'] = fix_path(entry['label'])

    with open(updated_json_path, 'w') as f:
        json.dump(dataset, f, indent=4)
    print(f"\nUpdated JSON saved to: {updated_json_path}")


# Paths you provide
original_data_dir = './dataset'
unzipped_data_dir = './dataset_unzipped'
original_json = './dataset/dataset.json'
updated_json = './dataset_unzipped/dataset_unzipped.json'

# 1. Decompress all .nii.gz files
unzip_nii_gz_folder(original_data_dir, unzipped_data_dir)

# 2. Update JSON to point to .nii files
update_dataset_json(original_json, updated_json, original_data_dir, unzipped_data_dir)
