# Project MIRROR 🪞 | Theory of Mind AI

**Project MIRROR** is an advanced "Secure Cognitive Infrastructure" that revolutionizes human-AI interaction. By decoupling analysis from conversation, MIRROR builds a real-time "Theory of Mind" of the user to deliver 100% personalized mentoring.

---

## 🌊 Life of a Message: The Shadow-Loop Trace
How data moves through Project MIRROR in every turn:

1.  **Input:** `app.py` (Streamlit) captures the user query and markdown-formatted physics prompts.
2.  **Analysis:** `src/agents.py` (**Observer 3B**) intercepts the query, extracting cognitive load, knowledge gaps, and vibe into a structured JSON payload.
3.  **Persistence:** `src/storage_manager.py` updates the **Cognological Ledger** (`data/session_mirror.json`) with a chronological snapshot.
4.  **Calibration:** The `storage_manager` weaves a context summary of the last 3 turns, which is injected into the **Actor 8B**'s system prompt along with the Observer's strategy.
5.  **Response:** `src/agents.py` (**Actor 8B**) generates the final pedagogically-aligned reply using its "Call-Back" voice.

---

## 🗺️ Component Map

| File | Responsibility | Core Tech |
| :--- | :--- | :--- |
| `app.py` | The "Glass Box" UI & Dashboard | Streamlit, Pandas |
| `main.py` | CLI Entry point & Loop Orchestrator | Python, Torch |
| `src/agents.py` | The Dual-Agent Cognitive Engine | Unsloth, Llama 3.1/3.2 |
| `src/storage_manager.py` | Persistence & Context Weaving | JSON, Python |
| `prompts/` | Systematic Personas & Strategies | Plaintext Templates |
| `data/` | The Chronological Cognitive Ledger | JSON Snapshots |

---

## ⚙️ Hardware Optimization (RTX 4050)
Project MIRROR is engineered for ultra-fast performance on **6GB VRAM** consumer hardware:

*   **Unsloth 4-bit Quantization:** Fits 11B combined parameters (3B + 8B) with room for context.
*   **Sequential Inference turns:** Uses a manual memory-clearing bridge (`torch.cuda.empty_cache()`) to swap models in and out of the active kernel space without OOM errors.
*   **Triton Kernels:** Leverages Unsloth's optimized generation kernels for 2x faster token throughput compared to standard HuggingFace implementations.

---

## 🚀 Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the hardware pre-flight: `python main.py`
3. Launch the dashboard: `streamlit run app.py`

*Built for the future of empathetic AI.*
