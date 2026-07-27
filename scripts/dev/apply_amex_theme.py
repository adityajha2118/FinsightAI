import os
import glob

def apply_amex_theme():
    # Find all page.tsx in the dashboard directory
    pages = glob.glob('finsight-frontend/src/app/(dashboard)/**/page.tsx', recursive=True)
    
    replacements = {
        # Tailwind text colors
        'text-white': 'text-amex-gray-900',
        'text-slate-400': 'text-amex-gray-600',
        'text-slate-500': 'text-amex-gray-600',
        'text-slate-600': 'text-amex-gray-300',
        'text-indigo-400': 'text-amex-blue',
        'text-indigo-300': 'text-amex-blue-dark',
        'text-rose-400': 'text-amex-red',
        'text-emerald-400': 'text-amex-green',
        'text-amber-400': 'text-amex-amber',
        
        # Hex Colors used in KpiCards & ChartCards
        '#6366f1': '#006FCF',  # Indigo to Amex Blue
        '#3b82f6': '#006FCF',  # Blue to Amex Blue
        '#10b981': '#008000',  # Emerald to Amex Green
        '#f43f5e': '#C0001A',  # Rose to Amex Red
        '#ef4444': '#C0001A',  # Red to Amex Red
        '#f59e0b': '#C07000',  # Amber to Amex Amber
        '#8b5cf6': '#004A8F',  # Purple to Amex Dark Blue
        '#f1f5f9': '#ffffff',  # Slate-100 to White (for text in charts)
    }

    count = 0
    for file_path in pages:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for old, new in replacements.items():
            new_content = new_content.replace(old, new)
            
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
            count += 1
            
    print(f"Applied Amex theme to {count} files.")

if __name__ == "__main__":
    apply_amex_theme()
