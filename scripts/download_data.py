"""
FinSight AI — Dataset Downloader
Downloads all raw datasets from Google Drive to data/raw/

Usage:
  python scripts/download_data.py

Requirements:
  pip install gdown
"""

import os
import subprocess
import sys

# ── Google Drive File IDs ───────────────────────────────────
# After uploading to Drive, replace each None with the file ID
# File ID is the part after /d/ in the shareable link:
# https://drive.google.com/file/d/FILE_ID_HERE/view
DRIVE_FILES = {
    "data/raw/customer/customer_data.csv":             None,  # REPLACE
    "data/raw/transactions/transactions.csv":           None,  # REPLACE
    "data/raw/transactions/bank_transactions.csv":      None,  # REPLACE
    "data/raw/campaign/bank_campaign.csv":              None,  # REPLACE
    "data/raw/kyc/kyc_part1.csv":                      None,  # REPLACE
    "data/raw/kyc/kyc_part2.csv":                      None,  # REPLACE
    "data/raw/complaints/cfpb_complaints.csv":          None,  # REPLACE
}


def download_all():
    try:
        import gdown
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip",
                               "install", "gdown", "-q"])
        import gdown

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for rel_path, file_id in DRIVE_FILES.items():
        dest = os.path.join(root, rel_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        if os.path.exists(dest):
            print(f"✓ Already exists: {rel_path}")
            continue

        if file_id is None:
            print(f"⚠️  No Drive ID set for: {rel_path}")
            print(f"   Upload to Google Drive and add the file ID to this script.")
            continue

        print(f"⬇️  Downloading: {rel_path}")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, dest, quiet=False)
        print(f"✓  Saved: {dest}")

    print("\nAll downloads complete.")
    print("Run notebooks in order: 01 → 13")


if __name__ == "__main__":
    download_all()
