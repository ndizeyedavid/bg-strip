<!-- <div align="center"> -->

```text

        ██████╗  ██████╗     ███████╗████████╗██████╗ ██╗ ██████╗
        ██╔══██╗██╔════╝     ██╔════╝╚══██╔══╝██╔══██╗██║ ██╔══██╗
        ██████╔╝██║  ███╗    ███████╗   ██║   ██████╔╝██║ ██████╔╝
        ██╔══██╗██║   ██║    ╚════██║   ██║   ██╔══██╗██║ ██╔═══╝
        ██████╔╝╚██████╔╝    ███████║   ██║   ██║  ██║██║ ██║
        ╚═════╝  ╚═════╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═╝

        ⚡ Native High-Performance AI Segmentation Suite ⚡

```

<!-- </div> -->

## Key Features

- **Immersive Terminal UI:** Fully keyboard-navigable interactive selection menus, simulated loader sequences, and micro-spinner animations inspired by modern developer ecosystems.
- **SOTA Neural Models:** Supports multiple commercial-grade architectures out of the box, including `BiRefNet` (for difficult edges like flying hair strands) and `BRIA RMBG-1.4`.
- **Dual-Execution Pipeline:** Toggle seamlessly between an interactive arrow-key selection dashboard and automated, inline script parameters (`-i` / `-o`) for headless server environments.
- **Hardware Accelerated:** Built directly over the C++ ONNX Runtime; supports local CPU multithreading or high-speed NVIDIA CUDA GPU acceleration pipelines automatically.
- **Granular Real-time Analytics:** Includes step-by-step progress tickers and compiles a comprehensive summary report highlighting total runtime, throughput rate, and file conversion successes.

---

## Installation & Setup

Ensure you have **Python 3.10+** set up on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/ndizeyedavid/bg-strip.git
cd bg-strip

```

### 2. Configure a Virtual Environment

```bash
python -m venv bg_env

# On Windows (Command Prompt / PowerShell)
.\bg_env\Scripts\activate

# On macOS / Linux
source bg_env/bin/activate

```

### 3. Install Dependencies

Choose the configuration matching your system's hardware specifications:

```bash
# Option A: For NVIDIA GPU Acceleration (Blazing Fast)
pip install rembg[gpu] pillow click tqdm colorama InquirerPy

# Option B: For Standard CPU Processing
pip install rembg pillow click tqdm colorama InquirerPy

```

---

## How to Run

### Interactive Dashboard (Recommended)

Simply launch the engine without any arguments. It will greet you with the custom ASCII splash screen and guide you through selecting inputs and models via your keyboard arrow keys:

```bash
python bg_strip.py

```

### Mode B: Direct CLI Execution (Fast Batching)

Pass automated flags to explicitly bypass the interactive prompt for scripting or quick directory clearing:

```bash
# Process an entire folder directory
python bg_strip.py -i "./raw_photos" -o "./finished_pngs" -m rmbg

# Automatically strip all images in the folder you are currently standing in
python bg_strip.py --all

```

---

## Supported Models

| Flag Name          | Model Architecture          | Primary Use-Case                                                |
| ------------------ | --------------------------- | --------------------------------------------------------------- |
| `birefnet-general` | Bilateral Reference Network | Ultra-detailed segmentation (Hair, threads, complex structures) |
| `rmbg`             | BRIA RMBG-1.4               | High-fidelity, rapid commercial application output              |
| `u2net`            | U2Net                       | Classic, balanced standard baseline silhouette cutting          |

> **Note on Initial Run:** The first time you call a model architecture, the system will securely stream and cache the model weight files from Hugging Face onto your machine. Subsequent executions require zero internet access and process instantly from disk.
