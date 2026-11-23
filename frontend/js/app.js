let activeMainFeature = 'conversion';
let activeConversionTool = 'pdf-to-docx';
let selectedFiles = [];
let originalImageObjectUrl = null;
let processedImageObjectUrl = null;
let currentResultBlob = null;
let currentResultFileName = '';

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
  const pdfControls = document.getElementById('pdfWatermarkControls');

  clearFile();

  if (feature === 'conversion') {
    subTabs.style.display = 'grid';
    pdfControls.style.display = 'none';
    setConversionSubTool(activeConversionTool);
  } else if (feature === 'enhancer') {
    subTabs.style.display = 'none';
    pdfControls.style.display = 'none';
    viewTitle.textContent = 'Image Enhancer';
    viewDesc.textContent = 'Improve clarity, sharpness, and color contrast of your photos.';
    fileInput.accept = '.png,.jpg,.jpeg,.webp';
    fileInput.multiple = false;
    dropzoneHint.textContent = '.png, .jpg, .webp up to 50 MB';
    document.getElementById('btnText').textContent = 'Enhance Image';
  } else if (feature === 'remover') {
    subTabs.style.display = 'none';
    pdfControls.style.display = 'none';
    viewTitle.textContent = 'Background Remover';
    viewDesc.textContent = 'Isolate foreground subjects and export transparent PNGs automatically.';
    fileInput.accept = '.png,.jpg,.jpeg,.webp';
    fileInput.multiple = false;
    dropzoneHint.textContent = '.png, .jpg, .webp up to 50 MB';
    document.getElementById('btnText').textContent = 'Remove Background';
  } else if (feature === 'watermark') {
    subTabs.style.display = 'none';
    pdfControls.style.display = 'none';
    viewTitle.textContent = 'Watermark Remover';
    viewDesc.textContent = 'Automatically detect and erase watermark text, logos, and stamps from photos or PDFs.';
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

  clearComparison();

  const preview = document.getElementById('filePreview');
  const fname = document.getElementById('fileName');
  const fmeta = document.getElementById('fileMeta');
  const ficon = document.getElementById('fileTypeIcon');
  const actionBtn = document.getElementById('actionBtn');
  const first = selectedFiles[0];
  const ext = first.name.split('.').pop().toLowerCase();

  if (['png', 'jpg', 'jpeg', 'webp'].includes(ext)) {
    if (originalImageObjectUrl) {
      URL.revokeObjectURL(originalImageObjectUrl);
    }
    originalImageObjectUrl = URL.createObjectURL(first);
  }

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

  const pdfControls = document.getElementById('pdfWatermarkControls');
  if (activeMainFeature === 'watermark' && ext === 'pdf') {
    pdfControls.style.display = 'block';
  } else {
    pdfControls.style.display = 'none';
  }

  hideStatus();
}

function clearFile() {
  selectedFiles = [];
  fileInput.value = '';
  
  if (originalImageObjectUrl) {
    URL.revokeObjectURL(originalImageObjectUrl);
    originalImageObjectUrl = null;
  }
  clearComparison();

  document.getElementById('filePreview').style.display = 'none';
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
      form.append('preset', 'auto');
      showStatus('info', 'Automatically detecting and removing watermarks...');
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
    let outName = fallbackOutName;
    const disposition = res.headers.get('Content-Disposition');
    if (disposition) {
      const m = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
      if (m && m[1]) outName = m[1].replace(/['"]/g, '');
    }

    const isImageTool = ['enhancer', 'remover', 'watermark'].includes(activeMainFeature);
    const isImageFile = selectedFiles[0] && ['.png', '.jpg', '.jpeg', '.webp'].some(ext => selectedFiles[0].name.toLowerCase().endsWith(ext));

    if (isImageTool && isImageFile && originalImageObjectUrl) {
      showImageComparison(originalImageObjectUrl, blob, outName, selectedFiles[0]);
    } else {
      triggerDirectDownload(blob, outName);
      showStatus('success', `Completed: ${outName}`);
    }
  } catch (err) {
    showStatus('error', err.message);
  } finally {
    actionBtn.disabled = !selectedFiles.length;
    btnIcon.className = 'fa-solid fa-play';
    btnText.textContent = originalText;
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  switchMainFeature('conversion');
});
