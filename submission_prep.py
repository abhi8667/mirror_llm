import os
import json

def sanitize_project():
    """Final Sanitization for Project MIRROR Submission."""
    print("--- 🪞 Project MIRROR: Submission Sanitization ---")
    
    # 1. Initialize Data Folder
    os.makedirs("data", exist_ok=True)
    with open("data/session_mirror.json", "w") as f:
        json.dump([], f)
    print("[SUCCESS] Cognitive Ledger initialized (empty).")

    # 2. Check for .env and sensitive keys
    if os.path.exists(".env"):
        print("[WARNING] .env file detected. Ensure it contains no leaked keys before pushing.")
        # Optional: Scrub specific patterns if needed
    
    # 3. Verify core files
    core_files = ["main.py", "app.py", "src/agents.py", "src/storage_manager.py", "requirements.txt"]
    for f in core_files:
        if os.path.exists(f):
            print(f"[VERIFIED] {f} found.")
        else:
            print(f"[MISSING] {f} not found!")

    print("\n[COMPLETE] Project MIRROR sanitized for release.")

if __name__ == "__main__":
    sanitize_project()
