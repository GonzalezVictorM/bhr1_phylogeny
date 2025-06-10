import requests
import json
import os

print("test")

# Configuration
BASE_URL = "https://files.jgi.doe.gov/mycocosm_file_list/"
ORGANISM_ID = "Dicsqu464_2"
FILES_PER_PAGE = 20

# File filter for 'best models' FASTA
FILE_FILTER = {
    "file_type": "fasta",
    "data_type": "proteins",
    "meta_content": "proteins_filtered",
    "file_status": "RESTORED"
}

# Request parameters
params = {
    "organism": ORGANISM_ID,
    "api_version": 2,
    "a": "false",  # Exclude archived files
    "h": "false",  # Exclude hidden files
    "d": "asc",    # Sort ascending
    "p": 1,        # Page 1
    "x": FILES_PER_PAGE,  # Files per page
    "t": "simple",  # Simple response format
    "ff": json.dumps(FILE_FILTER)  # JSON-encoded file filter
}

# Authentication headers
headers = {
    "accept": "application/json",
    "Authorization":  "test" # Replace with your personal token or use os.getenv("JGI_TOKEN")
}

def save_files():
    """Fetch and save paginated file lists from the MycoCosm API."""
    page = 1
    while True:
        params["p"] = page
        try:
            # Send API request
            print(f"Fetching page {page} for {ORGANISM_ID} with {FILES_PER_PAGE} files per page...")
            response = requests.get(BASE_URL, params=params, headers=headers)
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Validate response structure
            if not isinstance(data, dict) or "organisms" not in data or not data["organisms"]:
                print(f"Error: Unexpected response structure on page {page}")
                break
            files = data["organisms"][0].get("files", [])
            print(f"Page {page} contains {len(files)} files.")

            # Save JSON response to file
            output_file = f"file_list_page{page}.json"
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved page {page} to {output_file}")

            # Check for more pages
            next_page = data.get("next_page", False)
            file_total = data["organisms"][0].get("file_total", 0)
            print(f"Next page exists: {next_page}, Total files: {file_total}")

            # Stop if no more pages or all files fetched
            if not next_page or page * FILES_PER_PAGE >= file_total:
                if len(files) > FILES_PER_PAGE:
                    print(f"Note: Page {page} returned {len(files)} files, exceeding x={FILES_PER_PAGE}. API may not support pagination for small result sets.")
                break

            page += 1

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error on page {page}: {e} (Status: {response.status_code}, Response: {response.text})")
            break
        except requests.exceptions.RequestException as e:
            print(f"Request Error on page {page}: {e}")
            break
        except (ValueError, KeyError) as e:
            print(f"Parsing Error on page {page}: {e}")
            break

def parse_files():
    """Parse saved JSON files to find the 'best models' FASTA file."""
    page = 1
    target_file = None
    while os.path.exists(f"file_list_page{page}.json"):
        try:
            with open(f"file_list_page{page}.json", "r") as f:
                data = json.load(f)
            
            # Validate response structure
            if not isinstance(data, dict) or "organisms" not in data or not data["organisms"]:
                print(f"Error: Invalid structure in file_list_page{page}.json")
                page += 1
                continue
            
            # Get files list
            files = data["organisms"][0].get("files", [])
            print(f"Parsing file_list_page{page}.json: {len(files)} files found.")

            # Search for the 'best models' FASTA
            for file in files:
                metadata = file.get("metadata", {})
                # Double-check metadata and file name
                if (metadata.get("jat_label") == "proteins_filtered" and
                    file.get("file_status") == "RESTORED" and
                    file.get("file_name", "").endswith(".aa.fasta.gz")):
                    target_file = {
                        "file_name": file.get("file_name"),
                        "file_id": file.get("file_id"),
                        "file_path": file.get("file_path"),
                        "page": page
                    }
                    break
            
            if target_file:
                break
            page += 1

        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading file_list_page{page}.json: {e}")
            page += 1
            continue

    if target_file:
        print("\nFound 'best models' FASTA file:")
        print(f"File Name: {target_file['file_name']}")
        print(f"File ID: {target_file['file_id']}")
        print(f"File Path: {target_file['file_path']}")
        print(f"Found on Page: {target_file['page']}")
    else:
        print("\nNo 'best models' FASTA file found with jat_label='proteins_filtered', status='RESTORED', and ending in '.aa.fasta.gz'.")

if __name__ == "__main__":
    print(f"Processing file list for {ORGANISM_ID}...")
    # Fetch files if JSON doesn't exist
    if not os.path.exists("file_list_page1.json"):
        print("No JSON files found. Fetching from API...")
        save_files()
    # Parse JSON files
    print("Parsing JSON files...")
    parse_files()