import json
import glob

def fix_notebook_renderers(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    modified = False
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])
            
            # Check if this cell imports plotly
            has_plotly = any('import plotly' in line for line in source)
            
            if has_plotly:
                # Check if we already injected the renderer setting
                already_has_renderer = any('pio.renderers.default' in line for line in source)
                
                if not already_has_renderer:
                    # We need to add the import and renderer setting
                    # Find where the imports end, or just append it
                    new_lines = [
                        "import plotly.io as pio\n",
                        "pio.renderers.default = 'png'\n"
                    ]
                    
                    # Append right after the first plotly import
                    import_idx = next(i for i, line in enumerate(source) if 'import plotly' in line)
                    source.insert(import_idx + 1, new_lines[0])
                    source.insert(import_idx + 2, new_lines[1])
                    
                    cell['source'] = source
                    modified = True
                    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')
        print(f"Fixed renderers in {filepath}")
    else:
        print(f"No changes needed for {filepath}")

if __name__ == "__main__":
    files = glob.glob('notebooks/**/*.ipynb', recursive=True)
    for f in files:
        fix_notebook_renderers(f)
