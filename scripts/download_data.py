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
    "data/raw/customer/customer_data.csv":             "195VAF0kajMmNt-JhlxDTymZHlV_QgSkV",
    "data/raw/transactions/transactions.csv":           "1MYxnhhHq1dGfZeJ8NP697xtjeGBlYg8e",
    "data/raw/transactions/bank_transactions.csv":      "1p3_Ft5RPtyS2bldOb7W56giwSsb_MTNY",
    "data/raw/campaign/bank_campaign.csv":              "1TcYuAAbAN7oKDfsYkvtnzJkYjx3Tcb3c",
    "data/raw/kyc/kyc_part1.csv":                      "1r6KtRFSI8I7C_uTzHJKvaw-Y1F9MQNZ8",
    "data/raw/kyc/kyc_part2.csv":                      "1STgf5eQg9_N94Jr1r-a3SEMjBM6jgLSz",
    "data/raw/complaints/cfpb_complaints.csv":          "14-2JpcvjEYra0Oy77R8CFFYn053uMVsG",
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
