import torch

def get_vram_report():
    """Utility to monitor VRAM usage in real-time on 6GB hardware."""
    if not torch.cuda.is_available():
        return "CUDA Not Available"
    
    allocated = torch.cuda.memory_allocated(0) / (1024**3)
    reserved = torch.cuda.memory_reserved(0) / (1024**3)
    max_reserved = torch.cuda.max_memory_reserved(0) / (1024**3)
    
    return (
        f"[VRAM Monitor] Allocated: {allocated:.2f}GB | "
        f"Reserved: {reserved:.2f}GB | "
        f"Peak: {max_reserved:.2f}GB"
    )

if __name__ == "__main__":
    print(get_vram_report())
