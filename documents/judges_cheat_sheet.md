# 🧠 Project MIRROR: Judge’s Q&A Cheat Sheet (Phase 10)

### 1. "Why use two models? Why not just use one large model with a complex system prompt?"
*   **10/10 Answer:** "Decoupling 'Analysis' from 'Reasoning' solves the 'Self-Correction Trap'. Large models often fail to monitor their own performance or the user's state while simultaneously generating a response. By using a 3B Observer, we get a dedicated 'Shadow Brain' that provides an unbiased cognitive audit of the user, which we then inject as a system constraint into the 8B Actor. It’s significantly more stable and allows us to use smaller, faster models to outperform one large, 'monolithic' model."

### 2. "How are you handling VRAM OOM errors on a 6GB card with an 8B and a 3B model?"
*   **10/10 Answer:** "We implemented 'Sequential VRAM Orchestration'. Using Unsloth for 4-bit quantization reduces the footprint, but the real key is our 'Memory Guard' logic. Between the Observer turn and the Actor turn, we force a `torch.cuda.empty_cache()` and `gc.collect()`. This clears fragmentation and ensures that while the Actor is reasoning, the Observer is 'asleep' and taking up minimal VRAM headroom."

### 3. "What happens if the Observer misinterprets the user's vibe? Does it break the Mentor?"
*   **10/10 Answer:** "We built a 'Robust Fallback' layer. If the Observer's JSON is malformed or its confidence score is low, the system defaults to a 'Neutral Mentor' state. Furthermore, the Actor is still a highly capable 8B model; the Observer's strategy is an *injection*, not a replacement. The Actor uses its own reasoning but is 'nudged' by the Observer's insights."

### 4. "Is the 'Cognitive Ledger' truly useful, or just a log?"
*   **10/10 Answer:** "It's our engine for 'Temporal Awareness'. In Phase 7, we implemented a 'Context Weaver' that summarizes past cognitive states. This allows the Actor to say things like, 'I noticed you struggled with this concept three turns ago.' It turns a chat into a longitudinal pedagogical relationship."

### 5. "Why is 'Local-First' important for this specific use case?"
*   **10/10 Answer:** "Privacy is the ultimate constraint here. We are extracting psychological data—frustration levels, knowledge gaps, and latent intent. On a cloud system, this is a massive privacy risk. By running on the edge, we guarantee that the user's 'Theory of Mind' never leaves their hardware. It’s also zero-latency, which is critical for maintaining the 'Mentor-Student' flow."
