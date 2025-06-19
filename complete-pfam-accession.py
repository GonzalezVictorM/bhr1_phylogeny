import pandas as pd

# -----------------------------
# Config
# -----------------------------
csv_file = "fungal_tf_domains.csv"
text_file = "hmm_models/Pfam-A.hmm"               # your input .txt file
output_file = "pfam_accessions.txt" # optional output

# ----------------------------- 
# Load Pfam accessions from CSV
# -----------------------------
df = pd.read_csv(csv_file)
accessions = set(df['accession'].dropna().astype(str))

# -----------------------------
# Scan text file for matching lines
# -----------------------------
matched_lines = []
with open(text_file, "r") as f:
    for line in f:
        if line.startswith("ACC"):
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] in accessions:
                matched_lines.append(line)

# -----------------------------
# Output results
# -----------------------------
with open(output_file, "w") as f_out:
    f_out.writelines(matched_lines)

print(f"✅ Found {len(matched_lines)} matching lines. Saved to: {output_file}")
