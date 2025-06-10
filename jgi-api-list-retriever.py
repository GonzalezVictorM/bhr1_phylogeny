import requests
import json
import os
import csv

# -------------------------
# Configuration
# -------------------------
BASE_URL = "https://files.jgi.doe.gov/mycocosm_file_list/"
ORGANISM_ID = "Dicsqu464_2"
FILES_PER_PAGE = 1000  # Large enough to get all in one go for small sets

# Request parameters (NO FILE FILTER)
params = {
    "organism": ORGANISM_ID,
    "api_version": 2,
    "a": "false",  # Exclude archived
    "h": "false",  # Exclude hidden
    "d": "asc",    # Sort ascending
    "p": 1,        # Page number
    "x": FILES_PER_PAGE,  # Files per page
    "t": "simple"
}

# Authentication headers
headers = {
    "accept": "application/json",
    "Authorization": "test"  # Replace with your token or os.getenv("JGI_TOKEN")
}

# -------------------------
# Fetch and save JSON file list
# -------------------------
def fetch_all_files():
    print(f"Fetching all files for {ORGANISM_ID} from JGI...")
    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        with open("all_files.json", "w") as f:
            json.dump(data, f, indent=2)
        print("✅ File list saved to all_files.json")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e} - {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"General error: {e}")

# -------------------------
# Parse and filter JSON file locally, then export to CSV
# -------------------------
def parse_and_export():
    if not os.path.exists("all_files.json"):
        print("No all_files.json found. Please run fetch_all_files() first.")
        return

    with open("all_files.json", "r") as f:
        data = json.load(f)

    files = data.get("organisms", [{}])[0].get("files", [])
    print(f"Parsing {len(files)} files...")

    found = []
    for file in files:
        metadata = file.get("metadata", {})
        if metadata.get("jat_label") == "proteins_filtered":
            found.append({
                "organism": ORGANISM_ID,
                "file_name": file.get("file_name"),
                "file_id": file.get("file_id"),
                "_id": file.get("_id"),
                "file_status": file.get("file_status"),
                "md5sum": file.get("md5sum"),
                "file_date": file.get("file_date")
            })

    if found:
        with open("proteins_filtered_files.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "organism", "file_name", "file_id", "_id", "file_status", "md5sum", "file_date"
            ])
            writer.writeheader()
            writer.writerows(found)
        print(f"✅ Exported {len(found)} matching files to proteins_filtered_files.csv")
    else:
        print("❌ No 'proteins_filtered' FASTA files found.")

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    if not os.path.exists("all_files.json"):
        fetch_all_files()

    parse_and_export()
