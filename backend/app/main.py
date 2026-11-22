from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.routes import router as conversion_router

app = FastAPI(
    title="FreeShits Conversion API",
    description="High-performance, stateless, zero-retention file conversion & image processing engine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversion_router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FreeShits Conversion Engine",
        "privacy": "Zero-Retention / Ephemeral"
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FreeShits — Free File & Image Tools</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:          #000000;
    --surface:     #0c0c0c;
    --surface-2:   #141414;
    --border:      #1f1f1f;
    --border-2:    #2a2a2a;
    --text:        #f3f4f6;
    --text-muted:  #737373;
    --text-dim:    #404040;
    --accent:      #ffffff;
    --accent-dim:  rgba(255,255,255,0.06);
    --accent-hover:rgba(255,255,255,0.1);
    --danger:      #ef4444;
    --success:     #22c55e;
    --radius:      8px;
    --radius-lg:   14px;
    --transition:  140ms ease;
  }

  html { scroll-behavior: smooth; }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    font-size: 14px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }

  /* ── Header & Navigation ── */
  header {
    position: sticky;
    top: 0;
    z-index: 50;
    height: 58px;
    display: flex;
    align-items: center;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
  }

  .nav-container {
    width: 100%;
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    color: var(--text);
  }

  .brand-badge {
    width: 28px;
    height: 28px;
    border-radius: 7px;
    background: var(--surface-2);
    border: 1px solid var(--border-2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: var(--text);
  }

  .brand-name {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: -0.3px;
  }

  /* Main Navigation Tabs */
  .nav-menu {
    display: flex;
    align-items: center;
    gap: 4px;
    list-style: none;
  }

  .nav-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    border-radius: var(--radius);
    color: var(--text-muted);
    background: transparent;
    border: none;
    font-family: inherit;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition);
  }

  .nav-btn:hover {
    color: var(--text);
    background: var(--accent-dim);
  }

  .nav-btn.active {
    color: var(--text);
    background: var(--surface-2);
    border: 1px solid var(--border-2);
  }

  .nav-btn i {
    font-size: 13px;
    opacity: 0.8;
  }

  .nav-btn.active i {
    opacity: 1;
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .btn-docs {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 6px 12px;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 500;
    text-decoration: none;
    transition: all var(--transition);
  }

  .btn-docs:hover {
    color: var(--text);
    border-color: var(--border-2);
    background: var(--accent-dim);
  }

  /* ── Main Layout ── */
  main {
    flex: 1;
    max-width: 720px;
    width: 100%;
    margin: 0 auto;
    padding: 56px 20px 80px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* ── Page Header ── */
  .section-header {
    text-align: center;
    margin-bottom: 32px;
  }

  .section-header h1 {
    font-size: 32px;
    font-weight: 650;
    letter-spacing: -0.8px;
    color: var(--text);
    margin-bottom: 8px;
  }

  .section-header p {
    color: var(--text-muted);
    font-size: 14px;
    max-width: 480px;
    margin: 0 auto;
  }

  /* ── Sub-Tool Tabs (For File Conversion) ── */
  .sub-tabs {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2px;
    background: var(--surface-2);
    padding: 3px;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    margin-bottom: 20px;
  }

  .sub-tab-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    padding: 10px 8px;
    border-radius: 10px;
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-family: inherit;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition);
  }

  .sub-tab-btn:hover {
    color: var(--text);
  }

  .sub-tab-btn.active {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border-2);
    box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  }

  .sub-tab-btn i {
    font-size: 13px;
  }

  /* ── Tool Card ── */
  .tool-card {
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
  }

  .card-body {
    padding: 24px;
  }

  /* ── Dropzone (Bulletproof Click & Drag) ── */
  .dropzone {
    border: 1.5px dashed var(--border-2);
    border-radius: var(--radius);
    padding: 40px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    cursor: pointer;
    transition: all var(--transition);
    position: relative;
    background: rgba(255,255,255,0.01);
  }

  .dropzone:hover, .dropzone.drag-over {
    border-color: rgba(255,255,255,0.3);
    background: var(--accent-hover);
  }

  .dropzone.has-file {
    border-color: rgba(34,197,94,0.4);
    background: rgba(34,197,94,0.02);
  }

  .dropzone input[type="file"] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
    width: 100%;
    height: 100%;
    z-index: 20;
  }

  .dropzone-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    pointer-events: none;
  }

  .dropzone-icon {
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-2);
    border-radius: 11px;
    background: var(--surface-2);
    color: var(--text-muted);
    font-size: 17px;
    transition: all var(--transition);
  }

  .dropzone-title {
    font-size: 14px;
    font-weight: 500;
    color: var(--text);
  }

  .dropzone-hint {
    font-size: 12px;
    color: var(--text-muted);
  }

  .btn-browse-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 4px;
    padding: 5px 14px;
    background: var(--surface-2);
    border: 1px solid var(--border-2);
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text);
  }

  /* ── Interactive Watermark Canvas Editor ── */
  .canvas-editor-container {
    display: none;
    flex-direction: column;
    gap: 12px;
    margin-top: 16px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
  }

  .canvas-toolbar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
  }

  .tool-btn-group {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .tool-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: var(--surface);
    border: 1px solid var(--border-2);
    border-radius: 6px;
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all var(--transition);
  }

  .tool-btn:hover {
    color: var(--text);
    border-color: rgba(255,255,255,0.25);
  }

  .tool-btn.active {
    background: rgba(34,197,94,0.12);
    border-color: rgba(34,197,94,0.6);
    color: #4ade80;
  }

  .brush-slider-group {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--text-muted);
  }

  .brush-slider-group input[type="range"] {
    accent-color: #ffffff;
    cursor: pointer;
    width: 80px;
  }

  .canvas-stage {
    position: relative;
    width: 100%;
    max-height: 440px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background: #000000;
    border: 1px solid var(--border);
    border-radius: 6px;
  }

  #mainCanvas {
    max-width: 100%;
    max-height: 420px;
    display: block;
    cursor: crosshair;
  }

  .canvas-hint-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11.5px;
    color: var(--text-muted);
    padding-top: 4px;
  }

  /* ── File Preview Row ── */
  .file-preview {
    display: none;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 14px;
    padding: 12px 14px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
  }

  .file-preview-info {
    display: flex;
    align-items: center;
    gap: 10px;
    overflow: hidden;
  }

  .file-preview-icon {
    width: 32px;
    height: 32px;
    border-radius: 7px;
    background: var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text);
    font-size: 14px;
    flex-shrink: 0;
  }

  .file-name {
    font-size: 13px;
    font-weight: 500;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 340px;
  }

  .file-meta {
    font-size: 11px;
    color: var(--text-muted);
  }

  .btn-remove {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 13px;
    transition: all var(--transition);
  }

  .btn-remove:hover { color: var(--danger); background: rgba(239,68,68,0.1); }

  /* ── PDF Custom Text Controls ── */
  .pdf-controls {
    display: none;
    margin-top: 14px;
    padding: 14px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
  }

  .custom-text-input {
    width: 100%;
    padding: 9px 12px;
    background: var(--surface);
    border: 1px solid var(--border-2);
    border-radius: 6px;
    color: var(--text);
    font-family: inherit;
    font-size: 12.5px;
    outline: none;
    transition: border var(--transition);
  }

  .custom-text-input:focus {
    border-color: rgba(255,255,255,0.4);
  }

  /* ── Card Footer & Actions ── */
  .card-footer {
    padding: 16px 28px;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .btn-action {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 11px 20px;
    background: #ffffff;
    color: #000000;
    border: none;
    border-radius: var(--radius);
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition);
  }

  .btn-action:hover:not(:disabled) {
    background: #e2e8f0;
  }

  .btn-action:disabled {
    opacity: 0.25;
    cursor: not-allowed;
    background: #555555;
    color: #888888;
  }

  .status-bar {
    display: none;
    align-items: center;
    gap: 9px;
    padding: 9px 12px;
    border-radius: var(--radius);
    font-size: 12px;
    font-weight: 450;
    flex: 1;
  }

  .status-bar.visible { display: flex; }

  .status-bar.info {
    background: var(--surface-2);
    color: var(--text-muted);
    border: 1px solid var(--border);
  }

  .status-bar.success {
    background: rgba(34,197,94,0.06);
    color: #4ade80;
    border: 1px solid rgba(34,197,94,0.18);
  }

  .status-bar.error {
    background: rgba(239,68,68,0.06);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.18);
  }

  /* ── Privacy Note ── */
  .privacy-footer {
    margin-top: 24px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-dim);
    font-size: 11.5px;
  }

  .privacy-footer i {
    font-size: 11px;
  }

  /* ── Global Footer ── */
  footer {
    border-top: 1px solid var(--border);
    padding: 20px 24px;
    text-align: center;
    font-size: 12px;
    color: var(--text-dim);
  }

  @media (max-width: 600px) {
    .sub-tabs { grid-template-columns: repeat(2, 1fr); }
    .nav-btn span { font-size: 12px; }
    .card-footer { flex-direction: column; }
    .status-bar { width: 100%; }
    .canvas-toolbar { flex-direction: column; align-items: flex-start; }
  }
</style>
</head>
<body>

<!-- Header Navigation -->
<header>
  <div class="nav-container">
    <a href="/" class="brand">
      <div class="brand-badge">
        <i class="fa-solid fa-layer-group"></i>
      </div>
      <span class="brand-name">FreeShits</span>
    </a>

    <!-- Top Navigation Features -->
    <ul class="nav-menu">
      <li>
        <button class="nav-btn active" id="nav-conversion" onclick="switchMainFeature('conversion')">
          <i class="fa-solid fa-arrows-split-up-and-left"></i>
          <span>File Conversion</span>
        </button>
      </li>
      <li>
        <button class="nav-btn" id="nav-enhancer" onclick="switchMainFeature('enhancer')">
          <i class="fa-solid fa-wand-magic-sparkles"></i>
          <span>Image Enhancer</span>
        </button>
      </li>
      <li>
        <button class="nav-btn" id="nav-remover" onclick="switchMainFeature('remover')">
          <i class="fa-solid fa-scissors"></i>
          <span>Background Remover</span>
        </button>
      </li>
      <li>
        <button class="nav-btn" id="nav-watermark" onclick="switchMainFeature('watermark')">
          <i class="fa-solid fa-eraser"></i>
          <span>Watermark Remover</span>
        </button>
      </li>
    </ul>

    <div class="nav-right">
      <a href="/docs" target="_blank" class="btn-docs">
        <i class="fa-solid fa-code"></i>
        <span>API Docs</span>
      </a>
    </div>
  </div>
</header>

<!-- Main Workspace -->
<main>
  <!-- Section Title -->
  <div class="section-header">
    <h1 id="viewTitle">File Conversion</h1>
    <p id="viewDesc">Convert PDF, Word documents, and images with layout preservation.</p>
  </div>

  <!-- Sub-Tabs for File Conversion -->
  <div class="sub-tabs" id="conversionSubTabs">
    <button class="sub-tab-btn active" id="tab-pdf-to-docx" onclick="setConversionSubTool('pdf-to-docx')">
      <i class="fa-regular fa-file-pdf"></i>
      <span>PDF to Word</span>
    </button>
    <button class="sub-tab-btn" id="tab-docx-to-pdf" onclick="setConversionSubTool('docx-to-pdf')">
      <i class="fa-regular fa-file-word"></i>
      <span>Word to PDF</span>
    </button>
    <button class="sub-tab-btn" id="tab-images-to-pdf" onclick="setConversionSubTool('images-to-pdf')">
      <i class="fa-regular fa-images"></i>
      <span>Images to PDF</span>
    </button>
    <button class="sub-tab-btn" id="tab-pdf-to-images" onclick="setConversionSubTool('pdf-to-images')">
      <i class="fa-solid fa-images"></i>
      <span>PDF to Images</span>
    </button>
  </div>

  <!-- Processing Card -->
  <div class="tool-card">
    <div class="card-body">
      <!-- Bulletproof Dropzone with z-indexed file input -->
      <div class="dropzone" id="dropzone">
        <input type="file" id="fileInput">
        <div class="dropzone-content">
          <div class="dropzone-icon" id="dropzoneIcon">
            <i class="fa-solid fa-arrow-up-from-bracket"></i>
          </div>
          <div>
            <div class="dropzone-title" id="dropzoneTitle">Drag &amp; drop file here, or click to browse</div>
            <div class="dropzone-hint" id="dropzoneHint">.pdf files only — up to 50 MB</div>
          </div>
          <div class="btn-browse-pill">
            <i class="fa-solid fa-folder-open"></i> Choose File
          </div>
        </div>
      </div>

      <!-- File Preview Row -->
      <div class="file-preview" id="filePreview">
        <div class="file-preview-info">
          <div class="file-preview-icon">
            <i class="fa-regular fa-file" id="fileTypeIcon"></i>
          </div>
          <div>
            <div class="file-name" id="fileName">document.pdf</div>
            <div class="file-meta" id="fileMeta">0 KB</div>
          </div>
        </div>
        <button class="btn-remove" onclick="clearFile()" title="Remove file">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Interactive Canvas Editor for Watermark Remover -->
      <div class="canvas-editor-container" id="canvasEditor">
        <div class="canvas-toolbar">
          <div class="tool-btn-group">
            <button type="button" class="tool-btn active" id="btnToolBrush" onclick="setEditorTool('brush')">
              <i class="fa-solid fa-paintbrush"></i> Brush
            </button>
            <button type="button" class="tool-btn" id="btnToolBox" onclick="setEditorTool('box')">
              <i class="fa-regular fa-square"></i> Box Select
            </button>
            <button type="button" class="tool-btn" id="btnToolAuto" onclick="setEditorTool('auto')">
              <i class="fa-solid fa-wand-magic-sparkles"></i> Auto-Detect
            </button>
            <button type="button" class="tool-btn" onclick="clearCanvasMask()">
              <i class="fa-solid fa-rotate-left"></i> Reset
            </button>
          </div>

          <div class="brush-slider-group" id="brushSliderGroup">
            <span>Size:</span>
            <input type="range" id="brushSize" min="6" max="60" value="22" oninput="updateBrushSize(this.value)">
            <span id="brushSizeVal">22px</span>
          </div>
        </div>

        <div class="canvas-stage">
          <canvas id="mainCanvas"></canvas>
          <!-- Offscreen mask canvas -->
          <canvas id="maskCanvas" style="display: none;"></canvas>
        </div>

        <div class="canvas-hint-bar">
          <span id="canvasHintText"><i class="fa-solid fa-circle-info"></i> Brush or box over the watermark to erase. Unselected areas remain 100% untouched.</span>
          <span id="maskPixelCount" style="color: #4ade80;">Ready</span>
        </div>
      </div>

      <!-- PDF Specific Watermark Input -->
      <div class="pdf-controls" id="pdfWatermarkControls">
        <div style="font-size: 12px; font-weight: 500; color: var(--text-muted); margin-bottom: 8px;">
          <i class="fa-solid fa-file-pdf"></i> Watermark Text to Purge across PDF Pages:
        </div>
        <input type="text" id="pdfCustomText" placeholder="e.g. CONFIDENTIAL, DRAFT, CamScanner (leave blank to purge all standard stamps)" class="custom-text-input">
      </div>
    </div>

    <!-- Action & Status Footer -->
    <div class="card-footer">
      <button class="btn-action" id="actionBtn" onclick="executeCurrentAction()" disabled>
        <i class="fa-solid fa-play" id="btnIcon"></i>
        <span id="btnText">Convert File</span>
      </button>
      <div class="status-bar" id="statusBar">
        <i id="statusIcon" class="fa-solid fa-circle-notch fa-spin"></i>
        <span id="statusMessage">Processing...</span>
      </div>
    </div>
  </div>

  <!-- Zero Retention Banner -->
  <div class="privacy-footer">
    <i class="fa-solid fa-shield-halved"></i>
    <span>Stateless &amp; Private: Files are processed in memory and purged immediately after download.</span>
  </div>
</main>

<footer>
  FreeShits &bull; Free File Conversion &amp; Image Processing
</footer>

<script>
  let activeMainFeature = 'conversion';
  let activeConversionTool = 'pdf-to-docx';
  let selectedFiles = [];

  // Canvas Editor State
  let editorTool = 'brush'; // 'brush' or 'box'
  let brushRadius = 22;
  let isDrawing = false;
  let boxStartX = 0, boxStartY = 0;
  let loadedImage = null;
  let hasUserMask = false;

  const mainCanvas = document.getElementById('mainCanvas');
  const maskCanvas = document.getElementById('maskCanvas');
  const mainCtx = mainCanvas.getContext('2d');
  const maskCtx = maskCanvas.getContext('2d');

  const conversionTools = {
    'pdf-to-docx': {
      endpoint: '/api/convert/pdf-to-docx',
      accept: '.pdf',
      multiple: false,
      title: 'PDF to Word',
      desc: 'Convert PDF files into editable Microsoft Word (.docx) documents.',
      hint: '.pdf files only — up to 50 MB',
      btnText: 'Convert to Word',
      outName: n => n.replace(/\.[^/.]+$/, '') + '.docx'
    },
    'docx-to-pdf': {
      endpoint: '/api/convert/docx-to-pdf',
      accept: '.docx,.doc',
      multiple: false,
      title: 'Word to PDF',
      desc: 'Convert Word (.docx, .doc) files into clean, readable PDF documents with 100% table & style fidelity.',
      hint: '.docx, .doc files — up to 50 MB',
      btnText: 'Convert to PDF',
      outName: n => n.replace(/\.[^/.]+$/, '') + '.pdf'
    },
    'images-to-pdf': {
      endpoint: '/api/convert/images-to-pdf',
      accept: '.png,.jpg,.jpeg,.webp',
      multiple: true,
      title: 'Images to PDF',
      desc: 'Merge multiple image files into a single standardized PDF with auto-orientation.',
      hint: '.png, .jpg, .webp — select single or multiple images',
      btnText: 'Merge into PDF',
      outName: () => 'converted_images.pdf'
    },
    'pdf-to-images': {
      endpoint: '/api/convert/pdf-to-images',
      accept: '.pdf',
      multiple: false,
      title: 'PDF to Images',
      desc: 'Extract every page of a PDF document as high-resolution 200 DPI PNG images.',
      hint: '.pdf files — bundled into a ZIP archive if multi-page',
      btnText: 'Extract Images',
      outName: n => n.replace(/\.[^/.]+$/, '') + '_pages.zip'
    }
  };

  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');

  function switchMainFeature(feature) {
    activeMainFeature = feature;

    document.querySelectorAll('.nav-menu .nav-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('nav-' + feature).classList.add('active');

    const subTabs = document.getElementById('conversionSubTabs');
    const viewTitle = document.getElementById('viewTitle');
    const viewDesc = document.getElementById('viewDesc');
    const dropzoneHint = document.getElementById('dropzoneHint');
    const canvasEditor = document.getElementById('canvasEditor');
    const pdfControls = document.getElementById('pdfWatermarkControls');

    clearFile();

    if (feature === 'conversion') {
      subTabs.style.display = 'grid';
      canvasEditor.style.display = 'none';
      pdfControls.style.display = 'none';
      setConversionSubTool(activeConversionTool);
    } else if (feature === 'enhancer') {
      subTabs.style.display = 'none';
      canvasEditor.style.display = 'none';
      pdfControls.style.display = 'none';
      viewTitle.textContent = 'Image Enhancer';
      viewDesc.textContent = 'Improve clarity, sharpness, and color contrast of your photos.';
      fileInput.accept = '.png,.jpg,.jpeg,.webp';
      fileInput.multiple = false;
      dropzoneHint.textContent = '.png, .jpg, .webp up to 50 MB';
      document.getElementById('btnText').textContent = 'Enhance Image';
    } else if (feature === 'remover') {
      subTabs.style.display = 'none';
      canvasEditor.style.display = 'none';
      pdfControls.style.display = 'none';
      viewTitle.textContent = 'Background Remover';
      viewDesc.textContent = 'Isolate foreground subjects and export transparent PNGs automatically.';
      fileInput.accept = '.png,.jpg,.jpeg,.webp';
      fileInput.multiple = false;
      dropzoneHint.textContent = '.png, .jpg, .webp up to 50 MB';
      document.getElementById('btnText').textContent = 'Remove Background';
    } else if (feature === 'watermark') {
      subTabs.style.display = 'none';
      viewTitle.textContent = 'Watermark Remover';
      viewDesc.textContent = 'Erase stamps, logos, and watermark text from photos with interactive brush, or purge watermark layers from PDFs.';
      fileInput.accept = '.png,.jpg,.jpeg,.webp,.pdf';
      fileInput.multiple = false;
      dropzoneHint.textContent = '.png, .jpg, .webp, or .pdf files — up to 50 MB';
      document.getElementById('btnText').textContent = 'Remove Watermark';
    }
  }

  function setConversionSubTool(tool) {
    activeConversionTool = tool;
    const cfg = conversionTools[tool];

    document.querySelectorAll('.sub-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tab-' + tool).classList.add('active');

    document.getElementById('viewTitle').textContent = cfg.title;
    document.getElementById('viewDesc').textContent = cfg.desc;
    document.getElementById('btnText').textContent = cfg.btnText;

    fileInput.accept = cfg.accept;
    fileInput.multiple = cfg.multiple;
    document.getElementById('dropzoneHint').textContent = cfg.hint;

    clearFile();
  }

  // File selection
  fileInput.addEventListener('change', function(e) {
    if (this.files && this.files.length > 0) {
      processFiles(this.files);
    }
  });

  dropzone.addEventListener('dragover', e => {
    e.preventDefault();
    dropzone.classList.add('drag-over');
  });

  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag-over'));

  dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processFiles(e.dataTransfer.files);
    }
  });

  function processFiles(files) {
    selectedFiles = Array.from(files);
    if (!selectedFiles.length) return;

    const preview = document.getElementById('filePreview');
    const fname = document.getElementById('fileName');
    const fmeta = document.getElementById('fileMeta');
    const ficon = document.getElementById('fileTypeIcon');
    const actionBtn = document.getElementById('actionBtn');
    const first = selectedFiles[0];
    const ext = first.name.split('.').pop().toLowerCase();

    fname.textContent = first.name;
    fmeta.textContent = formatBytes(first.size);

    const iconMap = {
      pdf: 'fa-regular fa-file-pdf',
      docx: 'fa-regular fa-file-word',
      doc: 'fa-regular fa-file-word',
      png: 'fa-regular fa-file-image',
      jpg: 'fa-regular fa-file-image',
      jpeg: 'fa-regular fa-file-image',
      webp: 'fa-regular fa-file-image'
    };
    ficon.className = iconMap[ext] || 'fa-regular fa-file';

    preview.style.display = 'flex';
    actionBtn.disabled = false;
    actionBtn.removeAttribute('disabled');

    dropzone.classList.add('has-file');
    document.getElementById('dropzoneTitle').textContent = first.name;
    document.getElementById('dropzoneHint').textContent = 'Click or drop to choose a different file';
    document.getElementById('dropzoneIcon').innerHTML = '<i class="fa-solid fa-circle-check" style="color: #4ade80;"></i>';

    const canvasEditor = document.getElementById('canvasEditor');
    const pdfControls = document.getElementById('pdfWatermarkControls');

    if (activeMainFeature === 'watermark') {
      if (ext === 'pdf') {
        canvasEditor.style.display = 'none';
        pdfControls.style.display = 'block';
      } else {
        // Image loaded into interactive canvas
        pdfControls.style.display = 'none';
        setupInteractiveCanvas(first);
      }
    } else {
      canvasEditor.style.display = 'none';
      pdfControls.style.display = 'none';
    }

    hideStatus();
  }

  // Setup interactive image canvas for watermark brushing
  function setupInteractiveCanvas(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = new Image();
      img.onload = function() {
        loadedImage = img;
        mainCanvas.width = img.width;
        mainCanvas.height = img.height;
        maskCanvas.width = img.width;
        maskCanvas.height = img.height;

        // Render image onto mainCanvas
        redrawMainCanvas();
        clearCanvasMask();

        document.getElementById('canvasEditor').style.display = 'flex';
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  function redrawMainCanvas() {
    if (!loadedImage) return;
    mainCtx.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
    mainCtx.drawImage(loadedImage, 0, 0);

    // Overlay mask with emerald green semi-transparency
    mainCtx.save();
    mainCtx.drawImage(maskCanvas, 0, 0);
    mainCtx.restore();
  }

  function clearCanvasMask() {
    maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
    hasUserMask = false;
    const pixelCount = document.getElementById('maskPixelCount');
    if (editorTool === 'auto') {
      if (pixelCount) pixelCount.textContent = 'Auto-Detect active';
    } else {
      if (pixelCount) pixelCount.textContent = 'Ready (Brush over watermark)';
    }
    redrawMainCanvas();
  }

  function setEditorTool(tool) {
    editorTool = tool;
    const btnBrush = document.getElementById('btnToolBrush');
    const btnBox = document.getElementById('btnToolBox');
    const btnAuto = document.getElementById('btnToolAuto');
    const slider = document.getElementById('brushSliderGroup');
    const hint = document.getElementById('canvasHintText');
    const pixelCount = document.getElementById('maskPixelCount');

    if (btnBrush) btnBrush.classList.toggle('active', tool === 'brush');
    if (btnBox) btnBox.classList.toggle('active', tool === 'box');
    if (btnAuto) btnAuto.classList.toggle('active', tool === 'auto');

    if (tool === 'auto') {
      if (slider) slider.style.display = 'none';
      clearCanvasMask();
      if (hint) hint.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> <strong>Smart Auto-Detect:</strong> automatically detects text & logo stamps and cleans them with zero landscape distortion.';
      if (pixelCount) pixelCount.textContent = 'Auto-Detect active';
    } else if (tool === 'brush') {
      if (slider) slider.style.display = 'flex';
      if (hint) hint.innerHTML = '<i class="fa-solid fa-paintbrush"></i> <strong>Brush:</strong> paint over watermark. Only brushed pixels are infilled; untouched areas remain 100% pixel-perfect.';
      if (pixelCount && !hasUserMask) pixelCount.textContent = 'Ready (Brush over watermark)';
    } else if (tool === 'box') {
      if (slider) slider.style.display = 'none';
      if (hint) hint.innerHTML = '<i class="fa-regular fa-square"></i> <strong>Box Select:</strong> drag a rectangle around watermark stamps to remove them cleanly.';
      if (pixelCount && !hasUserMask) pixelCount.textContent = 'Ready (Drag rectangle)';
    }
  }

  function updateBrushSize(val) {
    brushRadius = parseInt(val, 10);
    document.getElementById('brushSizeVal').textContent = val + 'px';
  }

  // Canvas Mouse Coordinates relative to actual canvas resolution
  function getCanvasCoords(e) {
    const rect = mainCanvas.getBoundingClientRect();
    const scaleX = mainCanvas.width / rect.width;
    const scaleY = mainCanvas.height / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    };
  }

  mainCanvas.addEventListener('mousedown', e => {
    isDrawing = true;
    const pt = getCanvasCoords(e);
    if (editorTool === 'brush') {
      paintStroke(pt.x, pt.y);
    } else {
      boxStartX = pt.x;
      boxStartY = pt.y;
    }
  });

  window.addEventListener('mouseup', e => {
    if (!isDrawing) return;
    isDrawing = false;
    if (editorTool === 'box') {
      const pt = getCanvasCoords(e);
      const bx = Math.min(boxStartX, pt.x);
      const by = Math.min(boxStartY, pt.y);
      const bw = Math.abs(pt.x - boxStartX);
      const bh = Math.abs(pt.y - boxStartY);
      if (bw > 4 && bh > 4) {
        // Draw box on mask
        maskCtx.fillStyle = 'rgba(34, 197, 94, 0.45)';
        maskCtx.fillRect(bx, by, bw, bh);
        maskCtx.strokeStyle = '#22c55e';
        maskCtx.lineWidth = 2;
        maskCtx.strokeRect(bx, by, bw, bh);
        hasUserMask = true;
        document.getElementById('maskPixelCount').textContent = 'Area selected';
        redrawMainCanvas();
      }
    }
  });

  mainCanvas.addEventListener('mousemove', e => {
    if (!isDrawing) return;
    const pt = getCanvasCoords(e);
    if (editorTool === 'brush') {
      paintStroke(pt.x, pt.y);
    } else {
      // Live box preview
      redrawMainCanvas();
      mainCtx.save();
      mainCtx.fillStyle = 'rgba(34, 197, 94, 0.3)';
      mainCtx.strokeStyle = '#22c55e';
      mainCtx.lineWidth = 2;
      const bx = Math.min(boxStartX, pt.x);
      const by = Math.min(boxStartY, pt.y);
      const bw = Math.abs(pt.x - boxStartX);
      const bh = Math.abs(pt.y - boxStartY);
      mainCtx.fillRect(bx, by, bw, bh);
      mainCtx.strokeRect(bx, by, bw, bh);
      mainCtx.restore();
    }
  });

  function paintStroke(x, y) {
    maskCtx.save();
    maskCtx.fillStyle = 'rgba(34, 197, 94, 0.45)';
    maskCtx.beginPath();
    maskCtx.arc(x, y, brushRadius, 0, Math.PI * 2);
    maskCtx.fill();
    maskCtx.restore();

    hasUserMask = true;
    document.getElementById('maskPixelCount').textContent = 'Watermark brushed';
    redrawMainCanvas();
  }

  function clearFile() {
    selectedFiles = [];
    fileInput.value = '';
    loadedImage = null;
    hasUserMask = false;
    
    document.getElementById('filePreview').style.display = 'none';
    document.getElementById('canvasEditor').style.display = 'none';
    document.getElementById('pdfWatermarkControls').style.display = 'none';

    const actionBtn = document.getElementById('actionBtn');
    actionBtn.disabled = true;
    actionBtn.setAttribute('disabled', 'true');

    dropzone.classList.remove('has-file');
    document.getElementById('dropzoneTitle').textContent = 'Drag & drop file here, or click to browse';
    document.getElementById('dropzoneIcon').innerHTML = '<i class="fa-solid fa-arrow-up-from-bracket"></i>';

    if (activeMainFeature === 'conversion') {
      const cfg = conversionTools[activeConversionTool];
      document.getElementById('dropzoneHint').textContent = cfg.hint;
    } else if (activeMainFeature === 'watermark') {
      document.getElementById('dropzoneHint').textContent = '.png, .jpg, .webp, or .pdf files — up to 50 MB';
    } else {
      document.getElementById('dropzoneHint').textContent = '.png, .jpg, .webp up to 50 MB';
    }

    hideStatus();
  }

  function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(2) + ' MB';
  }

  function showStatus(type, message) {
    const bar = document.getElementById('statusBar');
    const icon = document.getElementById('statusIcon');
    const msg = document.getElementById('statusMessage');

    bar.className = 'status-bar visible ' + type;
    msg.textContent = message;

    if (type === 'error') {
      icon.className = 'fa-solid fa-triangle-exclamation';
    } else if (type === 'success') {
      icon.className = 'fa-solid fa-circle-check';
    } else {
      icon.className = 'fa-solid fa-circle-notch fa-spin';
    }
  }

  function hideStatus() {
    document.getElementById('statusBar').classList.remove('visible');
  }

  // Execute processing & auto-download
  async function executeCurrentAction() {
    if (!selectedFiles.length) return;

    const actionBtn = document.getElementById('actionBtn');
    const btnIcon = document.getElementById('btnIcon');
    const btnText = document.getElementById('btnText');
    const originalText = btnText.textContent;

    actionBtn.disabled = true;
    btnIcon.className = 'fa-solid fa-circle-notch fa-spin';
    btnText.textContent = 'Processing...';
    showStatus('info', 'Processing on server — downloading automatically when ready.');

    let endpoint = '';
    let isMultiple = false;
    let fallbackOutName = 'processed_file';

    const form = new FormData();

    if (activeMainFeature === 'conversion') {
      const cfg = conversionTools[activeConversionTool];
      endpoint = cfg.endpoint;
      isMultiple = cfg.multiple;
      fallbackOutName = cfg.outName(selectedFiles[0].name);
    } else if (activeMainFeature === 'enhancer') {
      endpoint = '/api/convert/enhance-image';
      fallbackOutName = 'enhanced_' + selectedFiles[0].name;
    } else if (activeMainFeature === 'remover') {
      endpoint = '/api/convert/remove-bg';
      fallbackOutName = selectedFiles[0].name.replace(/\.[^/.]+$/, '') + '_no_bg.png';
    } else if (activeMainFeature === 'watermark') {
      endpoint = '/api/convert/remove-watermark';
      fallbackOutName = 'clean_' + selectedFiles[0].name;

      const ext = selectedFiles[0].name.split('.').pop().toLowerCase();
      if (ext === 'pdf') {
        const customTxt = document.getElementById('pdfCustomText').value;
        if (customTxt && customTxt.trim()) {
          form.append('custom_text', customTxt.trim());
        }
      } else {
        // Image watermark: check if user brushed a mask on canvas
        if (editorTool !== 'auto' && hasUserMask) {
          showStatus('info', 'Erasing selected watermark with pixel-level precision...');
          // Export pure black and white mask from maskCanvas
          const exportCanvas = document.createElement('canvas');
          exportCanvas.width = maskCanvas.width;
          exportCanvas.height = maskCanvas.height;
          const expCtx = exportCanvas.getContext('2d');
          expCtx.fillStyle = '#000000';
          expCtx.fillRect(0, 0, exportCanvas.width, exportCanvas.height);

          // Get image data from maskCanvas: any non-transparent pixel becomes pure white (#ffffff)
          const maskImgData = maskCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height);
          const outImgData = expCtx.getImageData(0, 0, exportCanvas.width, exportCanvas.height);
          for (let i = 0; i < maskImgData.data.length; i += 4) {
            if (maskImgData.data[i + 3] > 10) { // Has opacity
              outImgData.data[i] = 255;
              outImgData.data[i + 1] = 255;
              outImgData.data[i + 2] = 255;
              outImgData.data[i + 3] = 255;
            }
          }
          expCtx.putImageData(outImgData, 0, 0);
          form.append('mask_data', exportCanvas.toDataURL('image/png'));
        } else {
          showStatus('info', 'Auto-detecting and removing watermark stamps...');
          form.append('preset', 'auto');
        }
      }
    }

    if (isMultiple) {
      selectedFiles.forEach(f => form.append('files', f));
    } else {
      form.append('file', selectedFiles[0]);
    }

    try {
      const res = await fetch(endpoint, { method: 'POST', body: form });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Processing error' }));
        throw new Error(err.detail || 'Failed to process file');
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;

      let outName = fallbackOutName;
      const disposition = res.headers.get('Content-Disposition');
      if (disposition) {
        const m = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
        if (m && m[1]) outName = m[1].replace(/['"]/g, '');
      }

      a.download = outName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);

      showStatus('success', `Completed: ${outName}`);
    } catch (err) {
      showStatus('error', err.message);
    } finally {
      actionBtn.disabled = !selectedFiles.length;
      btnIcon.className = 'fa-solid fa-play';
      btnText.textContent = originalText;
    }
  }

  // Initialize
  switchMainFeature('conversion');
</script>
</body>
</html>"""
