import os
import pandas as pd
import sys
import shutil
import gzip

# -----------------------------
# Define and validate paths
# -----------------------------
proteome_dir = "proteome_files"
compressed_dir = os.path.join(proteome_dir, "compressed_files")
extracted_dir = os.path.join(proteome_dir, "extracted_files")

# Ensure required directories exist
required_dirs = [proteome_dir, compressed_dir]
for d in required_dirs:
    if not os.path.isdir(d):
        sys.exit(f"❌ Directory not found: {d}")


os.makedirs(extracted_dir, exist_ok=True)

# -----------------------------
# Load CSV and file list
# -----------------------------
proteome_data = pd.read_csv("proteome_list_orthofinder.csv")

# List all files in compressed_dir
proteome_file_list = os.listdir(compressed_dir)

# -----------------------------
# Find missing files
# -----------------------------
expected_files = proteome_data["compressed_file"].dropna().astype(str)
available_files = set(proteome_file_list)

missing_files = [f for f in expected_files if f not in available_files]

# -----------------------------
# Report missing files
# -----------------------------
if missing_files:
    missing_str = ", ".join(missing_files)
    sys.exit(f"❌ Missing files: {missing_str}")
else:
    print("✅ All expected files are present.")

# -----------------------------
# Extract each compressed file
# -----------------------------

# New column to store extracted file paths
extracted_files_column = []

for _, row in proteome_data.iterrows():
    compressed_name = row["compressed_file"]

    # Default value in case extraction fails
    extracted_path = ""

    if pd.isna(compressed_name):
        extracted_files_column.append(extracted_path)
        continue

    compressed_path = os.path.join(compressed_dir, compressed_name)

    # Determine output file name (remove .gz or .zip etc.)
    if compressed_name.endswith(".gz"):
        output_name = compressed_name[:-3]  # strip .gz
        output_path = os.path.join(extracted_dir, output_name)
        try:
            with gzip.open(compressed_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            print(f"✅ Extracted {compressed_name} to {output_path}")
            extracted_path = output_path
        except Exception as e:
            print(f"❌ Failed to extract {compressed_name}: {e}")

    elif compressed_name.endswith(".zip"):
        # Handle .zip (extract all)
        try:
            shutil.unpack_archive(compressed_path, extracted_dir)
            print(f"✅ Extracted {compressed_name} to {extracted_dir}")
            # Just store the dir in this case
            extracted_path = extracted_dir
        except Exception as e:
            print(f"❌ Failed to extract {compressed_name}: {e}")

    else:
        print(f"⚠️ Skipping unsupported file: {compressed_name}")

    extracted_files_column.append(extracted_path)

# -----------------------------
# Add extracted file column
# -----------------------------
proteome_data["extracted_file"] = extracted_files_column

# Optionally: save updated CSV
extracted_names_path = os.path.join(proteome_dir, "proteome_list_with_extracted_files.csv")
proteome_data.to_csv(extracted_names_path, index=False)
print(f"📁 Saved updated CSV: {extracted_names_path}")