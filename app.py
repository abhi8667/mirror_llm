"""
app.py: The Glass Box UI (Streamlit)
-------------------------------------
The official dashboard for Project MIRROR. 
This UI implements a 60/40 dual-panel layout to visualize the 'Shadow Brain' 
logic alongside the mentor conversation.
"""

import streamlit as st
import json
import os
import time
import torch
from src.agents import ObserverAgent, ActorAgent
from src.storage_manager import StorageManager

# UI Page Configuration
st.set_page_config(
    page_title="Project MIRROR | Theory of Mind", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom Glass Box CSS for high-impact aesthetics
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    .dev-console { font-family: 'Courier New', Courier, monospace; font-size: 12px; color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# Session State Management: Persists chat and telemetry during re-renders
if "messages" not in st.session_state:
    st.session_state.messages = []
if "observer_state" not in st.session_state:
    st.session_state.observer_state = None
if "telemetry" not in st.session_state:
    st.session_state.telemetry = {"tps": 0.0, "vram": 0.0}

@st.cache_resource
def load_mirror_engine():
    """One-time initialization of the local LLM stack."""
    storage = StorageManager("data/session_mirror.json")
    observer = ObserverAgent("prompts/observer_v1.txt")
    actor = ActorAgent("prompts/actor_base.txt")
    return storage, observer, actor

storage, observer, actor = load_mirror_engine()

# --- SIDEBAR: SYSTEM CONTROLS ---
with st.sidebar:
    st.title("🪞 MIRROR Controls")
    st.markdown("### Profile: RTX 4050 6GB")
    st.divider()
    
    show_raw_logic = st.toggle("Show Raw Observer logic", value=False)
    
    if st.button("🚨 CLEAR SESSION (VRAM Purge)"):
        st.session_state.messages = []
        st.session_state.observer_state = None
        if os.path.exists("data/session_mirror.json"):
            with open("data/session_mirror.json", "w") as f:
                json.dump([], f)
        torch.cuda.empty_cache()
        st.success("Ledger Wiped & VRAM Cleared.")
        st.rerun()
    
    st.divider()
    st.caption("Architecture: Shadow-Loop (Unsloth 4-bit)")

# --- DUAL-PANEL LAYOUT ---
col_chat, col_dash = st.columns([0.6, 0.4])

with col_chat:
    st.header("Human Interface")
    
    # Renders the conversational history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Capture
    if prompt := st.chat_input("Engage with the Anti-Gravity Mentor..."):
        
        # Safety Valve for live demo stability
        if not prompt.strip() or len(prompt) > 2000:
            st.error("Invalid Input (5-2000 chars required).")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        start_time = time.time()

        # Step 1: Observer Processing (Llama 3.2 3B)
        with st.spinner("🧠 [Shadow Loop] Stage 1: Extraction..."):
            recent_history = storage.get_recent_history(limit=3)
            state = observer.analyze(prompt, recent_history)
            st.session_state.observer_state = state
            
        # Step 2: Actor Processing (Llama 3.1 8B)
        with st.spinner("🚀 [Shadow Loop] Stage 2: Calibration..."):
            response = actor.respond(prompt, state, recent_history)
            storage.append_snapshot(prompt, state, response)

        end_time = time.time()
        
        # Performance Telemetry Logging
        duration = end_time - start_time
        total_tokens = (len(prompt) + len(response)) / 4
        st.session_state.telemetry["tps"] = total_tokens / duration if duration > 0 else 0
        st.session_state.telemetry["vram"] = torch.cuda.memory_reserved(0) / (1024**3)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.rerun()

# TELEMETRY DASHBOARD (The Technical Flex)
with st.expander("🛠️ PERFORMANCE TELEMETRY"):
    tps = st.session_state.telemetry["tps"]
    vram = st.session_state.telemetry["vram"]
    st.markdown(f"""
    <div class='dev-console'>
    > GPU: NVIDIA RTX 4050 6GB<br>
    > THROUGHPUT: {tps:.2f} tokens/sec<br>
    > VRAM RESERVATION: {vram:.2f} GB / 6.00 GB<br>
    > STATUS: Optimizing Kernels...
    </div>
    """, unsafe_allow_html=True)

with col_dash:
    st.header("The Shadow Brain")
    
    if st.session_state.observer_state:
        state = st.session_state.observer_state
        
        # Load Metric: Visualizes cognitive burden
        load_score = state.get("load_score", 5)
        st.metric(label="Cognitive Load (1-10)", value=f"{load_score}/10")
        st.progress(int(load_score) / 10.0)

        # Vibe Tracker Status
        st.info(f"**Detected Vibe:** {state.get('vibe', 'Neutral')}")

        # Misconception Box
        with st.warning("Active Knowledge Gap"):
            st.write(state.get("knowledge_gap", "No critical gaps."))

        # Strategy indicator
        st.success(f"**Injected Strategy:** {state.get('strategy_instruction', 'N/A')}")

        if show_raw_logic:
            st.divider()
            st.json(state)
    else:
        st.info("Awaiting interaction...")
