import json
import os
from datetime import datetime

class StorageManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def append_snapshot(self, user_input: str, state: dict, response: str):
        """Appends a new chronological snapshot to the ledger."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "observer_state": state,
            "actor_response": response
        }
        
        try:
            # Atomic-style update: Load, Append, Save
            # This ensures the list structure is maintained correctly
            with open(self.file_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            
            history.append(snapshot)
            
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Storage Error: {e}")

    def get_recent_history(self, limit=3):
        """Retrieves the last N entries for trend and temporal analysis."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            return history[-limit:]
        except Exception:
            return []

    def get_context_weave(self, limit=5):
        """Context Weaver: Synthesizes a chronological cognitive summary for Phase 7."""
        history = self.get_recent_history(limit=limit)
        if not history:
            return "Initial State: No prior cognitive history."
        
        weave = []
        for i, entry in enumerate(history):
            # Extract only the critical subtext for VRAM-safe context
            vibe = entry['observer_state'].get('vibe', 'N/A')
            gap = entry['observer_state'].get('knowledge_gap', 'N/A')
            weave.append(f"Turn {i+1} Snapshot: Vibe={vibe} | Misconception={gap}")
            
        return "\n".join(weave)
