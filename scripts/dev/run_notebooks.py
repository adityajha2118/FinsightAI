"""Execute a notebook using nbconvert programmatically."""
import sys, os, traceback
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

os.environ['PYTHONIOENCODING'] = 'utf-8'

def run_notebook(nb_path, timeout=600):
    """Execute a notebook and save in-place."""
    print(f"Executing {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
    try:
        ep.preprocess(nb, {'metadata': {'path': '.'}})
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"  OK: {nb_path} executed successfully")
        return True
    except Exception as e:
        print(f"  FAIL: {nb_path}")
        traceback.print_exc()
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        return False

if __name__ == "__main__":
    notebooks = sys.argv[1:]
    for nb_path in notebooks:
        run_notebook(nb_path)
