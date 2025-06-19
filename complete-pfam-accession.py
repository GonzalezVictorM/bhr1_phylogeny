import pandas as pd

# -----------------------------
# Config
# -----------------------------
csv_file = "fungal_tf_domains.csv"
hmm_file = "hmm_models/Pfam-A.hmm"

# -----------------------------
# Parse full ACCs from HMM file
# -----------------------------
full_accession_map = {}

with open(hmm_file, "r") as f:
    for line in f:
        if line.startswith("ACC"):
            parts = line.strip().split()
            if len(parts) >= 2:
                full_acc = parts[1]           # e.g., PF00172.23
                base_acc = full_acc.split(".")[0]  # e.g., PF00172
                full_accession_map[base_acc] = full_acc

# -----------------------------
# Load and update the CSV
# -----------------------------
df = pd.read_csv(csv_file)

# Replace accessions with full versions if available
df["accession"] = df["accession"].astype(str).str.strip()
df["accession"] = df["accession"].apply(
    lambda acc: full_accession_map.get(acc, acc)
)

# -----------------------------
# Save updated CSV
# -----------------------------
df.to_csv(csv_file, index=False)
print(f"✅ Updated CSV saved to: {csv_file}")
