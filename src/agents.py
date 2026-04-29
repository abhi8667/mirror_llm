"""
src/agents.py: The Multi-Agent Cognitive Engine
-----------------------------------------------
This module implements the dual-agent "Shadow Loop" architecture.
Architecture:
- Observer (3B): Llama-3.2-3B-Instruct optimized with Unsloth 4-bit kernels.
- Actor (8B): Llama-3.1-8B-Instruct optimized with Unsloth 4-bit kernels.

VRAM Management Strategy:
To fit ~11B total parameters into 6GB of VRAM (RTX 4050), we use:
1. 4-bit quantization via bitsandbytes.
2. Sequential inference: The Observer and Actor never run concurrently.
3. Aggressive Cache Purging: Manual torch.cuda.empty_cache() between turns.
"""

import os
import json
import re
import gc
import torch
from unsloth import FastLanguageModel

# Model Configuration for RTX 4050 (6GB VRAM)
MAX_SEQ_LENGTH = 2048
DTYPE = None
LOAD_IN_4BIT = True

def vram_guard():
    """VRAM Guard: Ensures we don't hit OOM on 6GB hardware by monitoring reserved memory."""
    reserved = torch.cuda.memory_reserved(0) / (1024**3)
    if reserved > 5.5:
        # Trigger deep purge if memory reservation exceeds safety threshold
        torch.cuda.empty_cache()
        gc.collect()

def memory_optimized(func):
    """Decorator: Enforces aggressive memory clearing before and after every inference."""
    def wrapper(*args, **kwargs):
        vram_guard()
        torch.cuda.empty_cache()
        gc.collect()
        
        result = func(*args, **kwargs)
        
        # Immediate cleanup post-inference
        torch.cuda.empty_cache()
        gc.collect()
        return result
    return wrapper

class ObserverAgent:
    """
    The Observer (Shadow Brain):
    Tasked with Latent State Extraction. It analyzes user psychology, 
    cognitive load, and knowledge gaps without directly answering the user.
    """
    def __init__(self, prompt_path: str):
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Observer System Prompt missing: {prompt_path}")
            
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
            
        print("[SYSTEM] Initializing Observer (3B Analyst)...")
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name="unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
            max_seq_length=MAX_SEQ_LENGTH,
            dtype=DTYPE,
            load_in_4bit=LOAD_IN_4BIT,
        )
        FastLanguageModel.for_inference(self.model)

    def get_default_state(self) -> dict:
        """Fallback logic to ensure system stability if extraction fails."""
        return {
            "knowledge_gap": "None detected.",
            "load_score": 5,
            "vibe": "Neutral",
            "strategy_instruction": "Maintain standard mentor persona."
        }

    def clean_json_extraction(self, raw_output: str) -> dict:
        """
        Regex JSON Extraction:
        Local models often wrap JSON in conversational text ('chatter').
        This logic isolates the first '{' to last '}' block and parses it.
        """
        try:
            json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            return json.loads(raw_output)
        except (json.JSONDecodeError, AttributeError):
            return self.get_default_state()

    @memory_optimized
    def analyze(self, user_input: str, recent_history: list = None) -> dict:
        """Performs Latent State Extraction with Phase 7 Trend Awareness."""
        history_weave = "Initial session. No prior trajectory."
        if recent_history:
            history_weave = "\n".join([
                f"Turn {i+1}: Vibe={h.get('observer_state', {}).get('vibe')} | Gap={h.get('observer_state', {}).get('knowledge_gap')}"
                for i, h in enumerate(recent_history)
            ])

        try:
            messages = [
                {
                    "role": "system", 
                    "content": (
                        f"{self.system_prompt}\n\n"
                        "--- COGNITIVE TRAJECTORY (PHASE 7) ---\n"
                        f"USER HISTORY:\n{history_weave}\n\n"
                        "CRITICAL: Output ONLY a JSON object."
                    )
                },
                {"role": "user", "content": user_input}
            ]
            
            inputs = self.tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
            ).to("cuda")

            outputs = self.model.generate(
                input_ids=inputs, max_new_tokens=256, use_cache=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            response_tokens = outputs[0][inputs.shape[-1]:]
            raw_content = self.tokenizer.decode(response_tokens, skip_special_tokens=True)
            return self.clean_json_extraction(raw_content)
        except Exception:
            return self.get_default_state()

class ActorAgent:
    """
    The Actor (Mentor Voice):
    The conversational face of Project MIRROR. It is calibrated turns-by-turn
    by the Observer's strategy instructions.
    """
    def __init__(self, base_prompt_path: str):
        with open(base_prompt_path, "r", encoding="utf-8") as f:
            self.base_prompt = f.read()
            
        print("[SYSTEM] Initializing Actor (8B Mentor)...")
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name="unsloth/Llama-3.1-8B-Instruct-bnb-4bit",
            max_seq_length=MAX_SEQ_LENGTH,
            dtype=DTYPE,
            load_in_4bit=LOAD_IN_4BIT,
        )
        FastLanguageModel.for_inference(self.model)
        self.history = []

    @memory_optimized
    def respond(self, user_input: str, observer_state: dict, recent_history: list = None) -> str:
        """Generates a response calibrated by the Shadow Brain's extraction."""
        
        # Extract Phase 7 instructions
        vibe = observer_state.get("vibe", "Neutral")
        strategy = observer_state.get("strategy_instruction", "Be helpful.")
        gap = observer_state.get("knowledge_gap", "N/A")
        
        # Memory Hook Synthesis
        memory_hooks = "New interaction."
        if recent_history:
            memory_hooks = "\n".join([
                f"History Snapshot: {h.get('observer_state', {}).get('vibe')} regarding {h.get('observer_state', {}).get('knowledge_gap')[:30]}..."
                for h in recent_history
            ])

        # Dynamic System Injection
        system_override = f"""
[SYSTEM OVERRIDE - COGNITIVE CALIBRATION ACTIVE]
VRAM-SAFE CONTEXT: {memory_hooks}
STRATEGY: {strategy} | VIBE: {vibe} | TARGET GAP: {gap}
---------------------------------
Respond using a 'Call-Back' voice. Start by referencing past concepts or metaphors.
"""
        full_system_prompt = self.base_prompt + "\n" + system_override
        
        messages = [{"role": "system", "content": full_system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})
        
        try:
            inputs = self.tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
            ).to("cuda")

            outputs = self.model.generate(
                input_ids=inputs, max_new_tokens=1024, use_cache=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            response_tokens = outputs[0][inputs.shape[-1]:]
            reply = self.tokenizer.decode(response_tokens, skip_special_tokens=True)
            
            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": reply})
            
            return reply
        except Exception as e:
            return f"Actor Error: {e}"