import os
import re

router_dir = r"c:\Users\HP\Desktop\AMEX_FinsightAI\FinSight-AI\backend\src"
routers = []
for root, _, files in os.walk(router_dir):
    for f in files:
        if f == "router.py":
            routers.append(os.path.join(root, f))

for router_path in routers:
    with open(router_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "from fastapi import APIRouter, HTTPException" not in content and "from fastapi import APIRouter, Query, HTTPException" not in content:
        content = content.replace("from fastapi import APIRouter", "from fastapi import APIRouter, HTTPException")
        content = content.replace("from fastapi import APIRouter, Query", "from fastapi import APIRouter, Query, HTTPException")
        content = content.replace("from fastapi import APIRouter, Request", "from fastapi import APIRouter, Request, HTTPException")
        
    # Find all route functions
    # Pattern: def function_name(...):\n    """..."""\n    return ...
    # We want to wrap the body in try/except
    
    # Let's do a more careful replacement using regex or ast. 
    # Since they are all very simple "return service.xxx()" or "return await predict...", we can just replace "    return " with "    try:\n        return " and add the except block.
    
    lines = content.split('\n')
    new_lines = []
    in_route = False
    for i, line in enumerate(lines):
        if line.startswith('@router.'):
            in_route = True
        
        if in_route and "return " in line and not line.strip().startswith('#'):
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}try:")
            new_lines.append(f"    {line}")
            new_lines.append(f"{indent}except Exception as e:")
            new_lines.append(f"{indent}    raise HTTPException(status_code=500, detail=str(e))")
            in_route = False
        else:
            new_lines.append(line)
            
    with open(router_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print(f"Updated {router_path}")
