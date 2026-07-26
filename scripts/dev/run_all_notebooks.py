import glob
import subprocess
import os

import sys

def run_notebooks():
    notebooks = glob.glob('notebooks/**/*.ipynb', recursive=True)
    total = len(notebooks)
    
    print(f"Found {total} notebooks to execute...")
    
    success = 0
    failed = []
    
    for i, nb in enumerate(notebooks, 1):
        print(f"[{i}/{total}] Executing {nb}...")
        try:
            nb_abs = os.path.abspath(nb)
            nb_dir = os.path.dirname(nb_abs)
            nb_base = os.path.basename(nb_abs)
            
            # Execute the notebook inplace
            result = subprocess.run(
                [
                    sys.executable, "-m", "nbconvert", 
                    "--execute", 
                    "--inplace", 
                    "--ExecutePreprocessor.timeout=1200", # 20 mins per notebook max
                    nb_base
                ],
                cwd=nb_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  [OK] Success")
                success += 1
            else:
                print(f"  [FAIL] Failed")
                print(f"    Error: {result.stderr.strip().split(chr(10))[-1]}")
                failed.append(nb)
        except Exception as e:
            print(f"  [FAIL] Failed to run command: {e}")
            failed.append(nb)
            
    print("\n--- Execution Summary ---")
    print(f"Successfully executed: {success}/{total}")
    if failed:
        print("Failed notebooks:")
        for f in failed:
            print(f" - {f}")

if __name__ == "__main__":
    run_notebooks()
