import subprocess
import time
import os

print("Starting FinSight AI Backend & Frontend...")

os.makedirs("models", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

backend_process = subprocess.Popen(["python", "main.py"])
print("Backend started on port 8000...")

time.sleep(5)

frontend_process = subprocess.Popen(["python", "-m", "streamlit", "run", "frontend/dashboard.py", "--server.port", "8501"])
print("Frontend started on port 8501...")

try:
    backend_process.wait()
except KeyboardInterrupt:
    print("Shutting down...")
    backend_process.terminate()
    frontend_process.terminate()
