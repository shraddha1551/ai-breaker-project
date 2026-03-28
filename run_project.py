import os

print("Starting Target App...")
os.system("python -m uvicorn target_app.app:app --reload")