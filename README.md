# FreeShits

> **Stateless, 100% private file conversion & media utility suite.**
> Files are processed directly in memory/ephemeral scratchpads and immediately purged after download.

---

## Features

- **File Conversions:**
  - PDF to Word (`.docx`)
  - Word (`.docx` / `.doc`) to PDF (Native Microsoft Word COM engine preserving all tables, borders, and layouts)
  - Images (`.png`, `.jpg`, `.webp`) to PDF
  - PDF to Images (200 DPI crisp PNG extraction or zip bundle)
- **Image Utilities:**
  - **Image Enhancer:** Auto-contrast dynamic range stretch + sharpness + vibrancy.
  - **Background Remover:** Instant subject cutouts via cached U2-Net ONNX session.
  - **Watermark Remover (Images & PDFs):**
    - Dual-detector smart auto-removal (detects color text and stamp edges without distorting landscape/scenery).
    - Interactive canvas brush & box-select editor for targeted inpainting.
    - PDF watermark annotation and text stamp purge.

---

## How to Run Manually

### Option 1: 1-Click Launcher (Windows)
Double-click [start.bat](file:///c:/Users/PC/Desktop/Khen/Khen/FreeShits/start.bat) from File Explorer, or in PowerShell run:
```powershell
.\run.ps1
```

### Option 2: Terminal (PowerShell / Command Prompt)

1. Open terminal and navigate to the project root:
   ```powershell
   cd "c:\Users\PC\Desktop\Khen\Khen\FreeShits"
   ```

2. Run the Uvicorn server:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
   ```

3. Open your browser:
   - **Web App:** [http://localhost:8000](http://localhost:8000)
   - **Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Running Verification Tests

To verify all conversion and processing pipelines:
```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\python.exe backend/tests/test_conversion.py
```

