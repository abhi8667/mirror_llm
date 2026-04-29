# Project MIRROR 🪞 | Theory of Mind AI

**Project MIRROR** is a local, privacy-first AI mentor that builds a real-time "Theory of Mind" of the user. A decoupled **Shadow Loop** runs two LLMs back-to-back on consumer hardware: a small **Observer** model silently analyses every message for cognitive load, knowledge gaps, and emotional vibe, then passes a structured strategy to a larger **Actor** model that delivers a fully personalised response.

Because both models run locally via [Unsloth](https://github.com/unslothai/unsloth) 4-bit quantisation, your private cognitive profile never leaves your machine.

---

## 🌊 Life of a Message: The Shadow-Loop Trace

1. **Input** – `app.py` (Streamlit) or `main.py` (CLI) captures the user query.
2. **Analysis** – `src/agents.py` (**Observer 3B** · `Llama-3.2-3B-Instruct`) intercepts the query and extracts cognitive load, knowledge gaps, and vibe into a structured JSON payload.
3. **Persistence** – `src/storage_manager.py` appends a timestamped snapshot to the **Cognitive Ledger** (`data/session_mirror.json`).
4. **Calibration** – A context summary of the last 3 turns is woven into the **Actor 8B**'s system prompt together with the Observer's strategy.
5. **Response** – `src/agents.py` (**Actor 8B** · `Llama-3.1-8B-Instruct`) generates the final pedagogically-calibrated reply.

---

## 🗺️ Component Map

| File | Responsibility | Core Tech |
| :--- | :--- | :--- |
| `app.py` | "Glass Box" UI & live dashboard | Streamlit |
| `main.py` | CLI entry point & loop orchestrator | Python, Torch |
| `src/agents.py` | Dual-agent cognitive engine (Observer + Actor) | Unsloth, Llama 3.1 / 3.2 |
| `src/storage_manager.py` | Persistence & context weaving | JSON, Python |
| `src/vram_monitor.py` | Real-time VRAM usage utility | Torch |
| `prompts/` | System personas & strategy templates | Plain text |
| `data/` | Chronological Cognitive Ledger | JSON snapshots |
| `submission_prep.py` | One-shot project sanitisation / reset script | Python |

---

## ⚙️ Hardware Requirements

| Requirement | Minimum |
| :--- | :--- |
| GPU | NVIDIA GPU with **6 GB VRAM** (tested on RTX 4050) |
| CUDA | 11.8 or later |
| RAM | 16 GB system RAM recommended |
| Python | 3.10 or later |

> **Why 6 GB?** Unsloth 4-bit quantisation fits the combined ~11 B parameters (3 B Observer + 8 B Actor) into 6 GB by running the two models *sequentially* and aggressively purging VRAM between turns.

---

## 🚀 Getting Started

### 1 · Clone the repository

```bash
git clone https://github.com/abhi8667/mirror_llm.git
cd mirror_llm
```

### 2 · Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

> Unsloth and bitsandbytes require a CUDA-capable GPU. If you hit installation issues, follow the [Unsloth installation guide](https://github.com/unslothai/unsloth#installation) for your specific CUDA version.

### 4 · Initialise the data directory

```bash
python submission_prep.py
```

This creates `data/session_mirror.json` (an empty ledger) and verifies all core files are present.

### 5 · (Optional) Create a `.env` file

A `.env` file is loaded automatically if present. You can use it to set environment variables, for example:

```
# .env – add any custom environment variables here
HF_TOKEN=your_huggingface_token   # only needed for gated models
```

---

## ▶️ Running the Project

### Option A – Streamlit Web UI (recommended)

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`). The dual-panel dashboard shows the live **Shadow Brain** analysis alongside the mentor conversation.

**Sidebar controls:**
- **Show Raw Observer logic** – toggles the raw JSON payload from the Observer.
- **CLEAR SESSION (VRAM Purge)** – wipes the conversation, resets the ledger, and calls `torch.cuda.empty_cache()`.

### Option B – CLI

```bash
python main.py
```

The CLI runs a hardware pre-flight check (GPU name + VRAM), then starts the interactive prompt loop. Type `exit` or `quit` to stop, or press `Ctrl+C`.

### Option C – VRAM diagnostic

```bash
python src/vram_monitor.py
```

Prints a snapshot of currently allocated, reserved, and peak VRAM.

---

## 🧠 How the Shadow Loop Works

```
User message
    │
    ▼
┌─────────────────────────────┐
│  Observer (Llama-3.2 3B)    │  ← reads system prompt from prompts/observer_v1.txt
│  Extracts:                  │
│  • knowledge_gap            │
│  • load_score (1–10)        │
│  • vibe                     │
│  • strategy_instruction     │
└──────────────┬──────────────┘
               │  JSON payload
               ▼
┌─────────────────────────────┐
│  StorageManager             │  ← appends snapshot to data/session_mirror.json
│  Provides last-3 context    │
└──────────────┬──────────────┘
               │  calibrated system prompt
               ▼
┌─────────────────────────────┐
│  Actor (Llama-3.1 8B)       │  ← reads base prompt from prompts/actor_base.txt
│  Generates personalised     │
│  mentor reply               │
└─────────────────────────────┘
```

VRAM is manually cleared (`torch.cuda.empty_cache()` + `gc.collect()`) between every Observer and Actor inference turn to prevent OOM errors on 6 GB hardware.

---

*Built for the future of empathetic AI.*
