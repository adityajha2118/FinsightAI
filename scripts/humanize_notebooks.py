import os
import glob
import json
import re

def humanize_notebooks():
    notebook_paths = glob.glob('notebooks/**/*.ipynb', recursive=True)
    print(f"Found {len(notebook_paths)} notebooks to process.")
    
    # Generic AI comments to remove
    ai_comments = [
        r"# Import necessary libraries\n?",
        r"# Load the dataset\n?",
        r"# Check for missing values\n?",
        r"# Display the first few rows\n?",
        r"# Print the shape\n?",
        r"# Plot.*\n?",
        r"# Let's explore.*\n?",
        r"import warnings\n?warnings\.filterwarnings\('ignore'\)\n?"
    ]
    
    for path in notebook_paths:
        with open(path, 'r', encoding='utf-8') as f:
            try:
                nb = json.load(f)
            except Exception as e:
                print(f"Error loading {path}: {e}")
                continue
                
        modified = False
        new_cells = []
        
        for idx, cell in enumerate(nb.get('cells', [])):
            # Process Markdown cells
            if cell['cell_type'] == 'markdown':
                content = "".join(cell.get('source', []))
                
                # If it's a 'Key Insights' section, we skip adding it to the new notebook
                if '## Key Insights' in content or '### Data Quality Notes' in content:
                    modified = True
                    continue
                    
                # Shorten generic goals/introductions
                if 'Goal:' in content:
                    content = re.sub(r'Goal: Understand .*', 'Goal: EDA', content)
                    modified = True
                    
                # Rewrite big headers
                if 'Exploratory Data Analysis' in content:
                    content = content.replace('Exploratory Data Analysis', 'EDA')
                    modified = True
                    
                cell['source'] = [content]
                
            # Process Code cells
            elif cell['cell_type'] == 'code':
                original_source = "".join(cell.get('source', []))
                new_source = original_source
                
                for pattern in ai_comments:
                    new_source = re.sub(pattern, '', new_source, flags=re.IGNORECASE)
                
                # Remove multiple blank lines left over
                new_source = re.sub(r'\n{3,}', '\n\n', new_source)
                new_source = new_source.lstrip('\n')
                
                if original_source != new_source:
                    # Re-split into lines
                    lines = new_source.splitlines(keepends=True)
                    cell['source'] = lines
                    modified = True
                    
            new_cells.append(cell)
            
        if modified:
            nb['cells'] = new_cells
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=1)
                # ensure ends with newline if necessary
            print(f"Updated: {path}")

if __name__ == '__main__':
    humanize_notebooks()
