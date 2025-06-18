from Bio import SeqIO
import pandas as pd
import os
import sys

# -----------------------------
# Output directory for renamed FASTA files
# -----------------------------
proteome_dir = "proteome_files"
renamed_dir = os.path.join(proteome_dir, "renamed_files")
os.makedirs(renamed_dir, exist_ok=True)

# Ensure required directories exist
required_dirs = [proteome_dir]
for d in required_dirs:
    if not os.path.isdir(d):
        sys.exit(f"❌ Directory not found: {d}")

# -----------------------------
# Load CSV and file list
# -----------------------------
input_csv = os.path.join(proteome_dir, "proteome_list_with_extracted_files.csv")
proteome_data = pd.read_csv(input_csv)

# Prepare columns
renamed_file_column = []
log_data = []

# -----------------------------
# Process each extracted FASTA
# -----------------------------
for _, row in proteome_data.iterrows():
    input_path = row.get("extracted_file", "")
    if not input_path or not os.path.isfile(input_path):
        renamed_file_column.append("")
        log_data.append({
            "file": os.path.basename(input_path) if input_path else "MISSING",
            "total_sequences": 0,
            "renamed_sequences": 0,
            "first_id_before": "MISSING",
            "first_id_after": "MISSING"
        })
        continue

    portal_name = row.get("portal", "").strip()
    if portal_name:
        output_file_name = f"{portal_name}.fasta"
    else:
        output_file_name = os.path.basename(input_path)
    
    output_path = os.path.join(renamed_dir, output_file_name)
    renamed_file_column.append(output_path)


    try:
        records = list(SeqIO.parse(input_path, "fasta"))
        total_seqs = len(records)
        renamed_count = 0
        first_original_id = records[0].id if records else ""
        first_renamed_id = ""

        for i, record in enumerate(records):
            original_id = record.id  # store before any change
            if record.id.startswith("jgi|"):
                parts = record.id.split("|")
                if len(parts) >= 3:
                    new_id = f"{parts[1]}-{parts[2]}"
                    record.id = new_id
                    record.description = new_id
                    renamed_count += 1
                    if i == 0:
                        first_renamed_id = new_id
            elif i == 0:
                # If not renamed but first, keep original as renamed
                first_renamed_id = original_id

        with open(output_path, "w") as fout:
            SeqIO.write(records, fout, "fasta")

        print(f"✅ Renamed {renamed_count}/{total_seqs} headers in: {output_path}")

        log_data.append({
            "file": os.path.basename(input_path),
            "total_sequences": total_seqs,
            "renamed_sequences": renamed_count,
            "first_id_before": first_original_id,
            "first_id_after": first_renamed_id
        })

    except Exception as e:
        print(f"❌ Failed to rename headers in {input_path}: {e}")
        renamed_file_column[-1] = ""
        log_data.append({
            "file": os.path.basename(input_path),
            "total_sequences": 0,
            "renamed_sequences": 0,
            "first_id_before": "ERROR",
            "first_id_after": "ERROR"
        })

# -----------------------------
# Save updated CSV with renamed file paths
# -----------------------------
proteome_data["renamed_file"] = renamed_file_column
output_path = os.path.join(proteome_dir, "proteome_list_with_renamed_files.csv")
proteome_data.to_csv(output_path, index=False)
print(f"📁 Updated CSV: {output_path}")

# -----------------------------
# Save detailed log
# -----------------------------
log_df = pd.DataFrame(log_data)
log_path = os.path.join(proteome_dir, "renaming_summary_log.csv")
log_df.to_csv(log_path, index=False)
print(f"📝 Log saved to: {log_path}")