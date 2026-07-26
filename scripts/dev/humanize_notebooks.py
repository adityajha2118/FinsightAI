import json
import glob
import re
import os

def clean_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    new_cells = []
    
    # Generic AI comment patterns
    bad_comments = [
        re.compile(r"^#\s*Import necessary libraries", re.IGNORECASE),
        re.compile(r"^#\s*Load the dataset", re.IGNORECASE),
        re.compile(r"^#\s*Display the first few rows", re.IGNORECASE),
        re.compile(r"^#\s*Check for missing values", re.IGNORECASE),
        re.compile(r"^#\s*Print the shape", re.IGNORECASE),
        re.compile(r"^#\s*Let'?s explore", re.IGNORECASE),
        re.compile(r"^#\s*Plot", re.IGNORECASE),
        re.compile(r"^#\s*Initialize", re.IGNORECASE),
    ]

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = "".join(cell['source'])
            
            # Skip Key Insights cells completely
            if "## Key Insights" in source or "### Key Insights" in source or "Executive Summary" in source:
                continue
            
            # Strip fluffy intro stuff
            if "Let's dive into" in source or "In conclusion" in source:
                source = re.sub(r"(?i)Let'?s dive into[^.]*\.", "", source)
                source = re.sub(r"(?i)In conclusion[^.]*\.", "", source)

            # Strip generic subheadings
            source = re.sub(r"(?i)### Data Quality Notes", "", source)

            # Tone down "Goal:"
            source = re.sub(r"(?i)Goal:\s*", "Obj: ", source)
            
            # Put back list of strings
            lines = source.split("\n")
            # add newline character back except for the last line
            cell['source'] = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
            
            # Skip empty cells
            if not any(line.strip() for line in cell['source']):
                continue
                
            new_cells.append(cell)
            
        elif cell['cell_type'] == 'code':
            new_source = []
            for line in cell['source']:
                is_bad = False
                for pattern in bad_comments:
                    if pattern.search(line.strip()):
                        is_bad = True
                        break
                if not is_bad:
                    # Also strip repetitive warnings ignore
                    if "warnings.filterwarnings('ignore')" in line:
                        continue
                    if "import warnings" in line:
                        continue
                    new_source.append(line)
            
            # if we stripped all lines, but there were lines originally, keep the cell just empty
            cell['source'] = new_source
            new_cells.append(cell)

    nb['cells'] = new_cells
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        # add newline at end of file to mimic jupyter standard
        f.write('\n')

if __name__ == "__main__":
    files = glob.glob('notebooks/**/*.ipynb', recursive=True)
    count = 0
    for f in files:
        print(f"Cleaning {f}...")
        clean_notebook(f)
        count += 1
    print(f"Cleaned {count} notebooks.")
