"""
main.py: The Shadow Loop Orchestrator
--------------------------------------
This script acts as the entry point for Project MIRROR.
It manages the pre-flight hardware checks and executes the sequential 
multi-agent loop (User -> Observer -> Actor).
"""

import os
import json
import torch
from dotenv import load_dotenv
from src.agents import ObserverAgent, ActorAgent
from src.storage_manager import StorageManager

def model_pre_flight():
    """Hardware Check: Verifies CUDA and VRAM availability for 6GB optimization."""
    print("[SYSTEM] Performing Hardware Audit...")
    if not torch.cuda.is_available():
        print("[CRITICAL] CUDA not detected. MIRROR requires an NVIDIA GPU.")
        return
        
    gpu_name = torch.cuda.get_device_name(0)
    vram_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"[SYSTEM] Hardware Detected: {gpu_name} ({vram_total:.2f}GB VRAM)")
    
    if os.path.exists(".env"):
        load_dotenv()
    print("[SYSTEM] Environment initialized.\n")

def main():
    print("-----------------------------------------------------")
    print("Project MIRROR: Multi-Agent Shadow Loop Active")
    print("-----------------------------------------------------\n")
    
    model_pre_flight()
    
    # Initialize Engine Components
    storage = StorageManager("data/session_mirror.json")
    observer = ObserverAgent("prompts/observer_v1.txt")
    actor = ActorAgent("prompts/actor_base.txt")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # The Shadow Loop Logic
            # 1. Retrieve historical cognitive trajectory
            recent_history = storage.get_recent_history(limit=3)

            # 2. Sequential Inference Turn 1: The Observer (Analysis)
            print("[SHADOW LOOP] Step 1: Extracting Latent Cognitive State...")
            state = observer.analyze(user_input, recent_history)
            
            # 3. Sequential Inference Turn 2: The Actor (Response)
            # Memory Management: Actor starts only after Observer is purged from active kernels
            print("[SHADOW LOOP] Step 2: Formulating Calibrated Response...")
            response = actor.respond(user_input, state, recent_history)
            
            # 4. Persistence Turn: Update Chronological Ledger
            storage.append_snapshot(user_input, state, response)
            
            print(f"\nMentor: {response}\n")

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
