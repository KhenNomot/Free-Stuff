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
    return """<!DOCTYPE html>
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
    background: rgba(0, 0, 0, 0.88);
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
    max-width: 680px;
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
    max-width: 440px;
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
    padding: 28px;
  }

  /* ── Dropzone ── */
  .dropzone {
    border: 1.5px dashed var(--border-2);
    border-radius: var(--radius);
    padding: 44px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    cursor: pointer;
    transition: all var(--transition);
    position: relative;
    gap: 12px;
    background: rgba(255,255,255,0.01);
  }

  .dropzone:hover, .dropzone.drag-over {
    border-color: rgba(255,255,255,0.25);
    background: var(--accent-hover);
  }

  .dropzone input[type="file"] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
    width: 100%;
    height: 100%;
  }

  .dropzone-icon {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border-2);
    border-radius: 10px;
    background: var(--surface-2);
    color: var(--text-muted);
    font-size: 16px;
  }

  .dropzone-title {
    font-size: 13.5px;
    font-weight: 500;
    color: var(--text);
  }

  .dropzone-hint {
    font-size: 12px;
    color: var(--text-muted);
  }

  /* ── File Preview ── */
  .file-preview {
    display: none;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 16px;
    padding: 12px 14px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
  }

  .file-preview.visible { display: flex; }

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
    color: var(--text-muted);
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
    padding: 4px 6px;
    border-radius: 4px;
    font-size: 13px;
    transition: all var(--transition);
  }

  .btn-remove:hover { color: var(--danger); }

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
    background: var(--text);
    color: var(--bg);
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

  <!-- Sub-Tabs for File Conversion (Only visible under File Conversion view) -->
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
      <!-- Drag & Drop Zone -->
      <div class="dropzone" id="dropzone">
        <input type="file" id="fileInput" onchange="handleFileSelect(event)">
        <div class="dropzone-icon">
          <i class="fa-solid fa-arrow-up-from-bracket" id="dropzoneIcon"></i>
        </div>
        <div>
          <div class="dropzone-title" id="dropzoneTitle">Drop file here, or click to browse</div>
          <div class="dropzone-hint" id="dropzoneHint">.pdf files only — up to 50 MB</div>
        </div>
      </div>

      <!-- File Preview Row -->
      <div class="file-preview" id="filePreview">
        <div class="file-preview-info">
          <div class="file-preview-icon">
            <i class="fa-regular fa-file" id="fileTypeIcon"></i>
          </div>
          <div>
            <div class="file-name" id="fileName">file.pdf</div>
            <div class="file-meta" id="fileMeta">1.2 MB</div>
          </div>
        </div>
        <button class="btn-remove" onclick="clearFile()" title="Remove file">
          <i class="fa-solid fa-xmark"></i>
        </button>
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
    <span>Stateless & Private: Files are processed in memory and purged immediately after download.</span>
  </div>
</main>

<footer>
  FreeShits &bull; Free File Conversion &amp; Image Processing
</footer>

<script>
  // State Management
  let activeMainFeature = 'conversion'; // 'conversion' | 'enhancer' | 'remover'
  let activeConversionTool = 'pdf-to-docx';
  let selectedFiles = [];

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
      desc: 'Convert Word (.docx, .doc) files into clean, readable PDF documents.',
      hint: '.docx, .doc files — up to 50 MB',
      btnText: 'Convert to PDF',
      outName: n => n.replace(/\.[^/.]+$/, '') + '.pdf'
    },
    'images-to-pdf': {
      endpoint: '/api/convert/images-to-pdf',
      accept: '.png,.jpg,.jpeg,.webp',
      multiple: true,
      title: 'Images to PDF',
      desc: 'Merge multiple image files into a single standardized PDF.',
      hint: '.png, .jpg, .webp — select single or multiple images',
      btnText: 'Merge into PDF',
      outName: () => 'converted_images.pdf'
    },
    'pdf-to-images': {
      endpoint: '/api/convert/pdf-to-images',
      accept: '.pdf',
      multiple: false,
      title: 'PDF to Images',
      desc: 'Extract every page of a PDF document as high-resolution PNG images.',
      hint: '.pdf files — bundled into a ZIP archive if multi-page',
      btnText: 'Extract Images',
      outName: n => n.replace(/\.[^/.]+$/, '') + '_pages.zip'
    }
  };

  // Switch between main navbar features
  function switchMainFeature(feature) {
    activeMainFeature = feature;

    // Update active nav button
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('nav-' + feature).classList.add('active');

    const subTabs = document.getElementById('conversionSubTabs');
    const viewTitle = document.getElementById('viewTitle');
    const viewDesc = document.getElementById('viewDesc');
    const btnText = document.getElementById('btnText');
    const fileInput = document.getElementById('fileInput');
    const dropzoneHint = document.getElementById('dropzoneHint');

    clearFile();

    if (feature === 'conversion') {
      subTabs.style.display = 'grid';
      setConversionSubTool(activeConversionTool);
    } else if (feature === 'enhancer') {
      subTabs.style.display = 'none';
      viewTitle.textContent = 'Image Enhancer';
      viewDesc.textContent = 'Improve clarity, sharpness, and color contrast of your photos.';
      fileInput.accept = '.png,.jpg,.jpeg,.webp';
      fileInput.multiple = false;
      dropzoneHint.textContent = '.png, .jpg, .webp up to 50 MB';
      btnText.textContent = 'Enhance Image';
    } else if (feature === 'remover') {
      subTabs.style.display = 'none';
      viewTitle.textContent = 'Background Remover';
      viewDesc.textContent = 'Isolate foreground subjects and export transparent PNGs automatically.';
      fileInput.accept = '.png,.jpg,.jpeg,.webp';
      fileInput.multiple = false;
      dropzoneHint.textContent = '.png, .jpg, .webp up to 50 MB';
      btnText.textContent = 'Remove Background';
    }
  }

  // Switch between conversion sub-tabs
  function setConversionSubTool(tool) {
    activeConversionTool = tool;
    const cfg = conversionTools[tool];

    document.querySelectorAll('.sub-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tab-' + tool).classList.add('active');

    document.getElementById('viewTitle').textContent = cfg.title;
    document.getElementById('viewDesc').textContent = cfg.desc;
    document.getElementById('btnText').textContent = cfg.btnText;

    const fileInput = document.getElementById('fileInput');
    fileInput.accept = cfg.accept;
    fileInput.multiple = cfg.multiple;
    document.getElementById('dropzoneHint').textContent = cfg.hint;

    clearFile();
  }

  // Drag and Drop listeners
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');

  dropzone.addEventListener('dragover', e => {
    e.preventDefault();
    dropzone.classList.add('drag-over');
  });

  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag-over'));

  dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) processFiles(e.dataTransfer.files);
  });

  function handleFileSelect(e) {
    if (e.target.files.length) processFiles(e.target.files);
  }

  function processFiles(files) {
    selectedFiles = Array.from(files);
    if (!selectedFiles.length) return;

    const preview = document.getElementById('filePreview');
    const fname = document.getElementById('fileName');
    const fmeta = document.getElementById('fileMeta');
    const ficon = document.getElementById('fileTypeIcon');
    const actionBtn = document.getElementById('actionBtn');

    if (selectedFiles.length === 1) {
      fname.textContent = selectedFiles[0].name;
      fmeta.textContent = formatBytes(selectedFiles[0].size);

      const ext = selectedFiles[0].name.split('.').pop().toLowerCase();
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
    } else {
      fname.textContent = `${selectedFiles.length} images selected`;
      const total = selectedFiles.reduce((s, f) => s + f.size, 0);
      fmeta.textContent = formatBytes(total) + ' total';
      ficon.className = 'fa-regular fa-images';
    }

    preview.classList.add('visible');
    actionBtn.disabled = false;
    hideStatus();
  }

  function clearFile() {
    selectedFiles = [];
    fileInput.value = '';
    document.getElementById('filePreview').classList.remove('visible');
    document.getElementById('actionBtn').disabled = true;
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

  // Execute processing
  async function executeCurrentAction() {
    if (!selectedFiles.length) return;

    const actionBtn = document.getElementById('actionBtn');
    const btnIcon = document.getElementById('btnIcon');
    const btnText = document.getElementById('btnText');
    const originalText = btnText.textContent;

    actionBtn.disabled = true;
    btnIcon.className = 'fa-solid fa-circle-notch fa-spin';
    btnText.textContent = 'Processing...';
    showStatus('info', 'Processing file on server — downloading automatically when complete.');

    let endpoint = '';
    let isMultiple = false;
    let fallbackOutName = 'processed_file';

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
    }

    const form = new FormData();
    if (isMultiple) {
      selectedFiles.forEach(f => form.append('files', f));
    } else {
      form.append('file', selectedFiles[0]);
    }

    try {
      const res = await fetch(endpoint, { method: 'POST', body: form });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Process failed' }));
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

  // Initialize view
  switchMainFeature('conversion');
</script>
</body>
</html>"""
