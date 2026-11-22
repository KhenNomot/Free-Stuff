from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.routes import router as conversion_router

app = FastAPI(
    title="FreeShits Conversion API",
    description="High-performance, stateless, zero-retention file conversion & image processing engine.",
    version="1.0.0"
)

# Enable CORS
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
    <title>FreeShits - Free File Converter</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#eef2ff',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
    <!-- Navbar -->
    <header class="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                    <i class="fa-solid fa-bolt text-white text-lg"></i>
                </div>
                <div>
                    <span class="font-bold text-lg tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">FreeShits</span>
                    <span class="ml-2 text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">v1.0 Local</span>
                </div>
            </div>
            <div class="flex items-center gap-4">
                <span class="inline-flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded-full border border-emerald-800">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    API Active
                </span>
                <a href="/docs" target="_blank" class="text-xs text-slate-400 hover:text-white transition flex items-center gap-1.5 bg-slate-800/60 px-3 py-1.5 rounded-lg border border-slate-700">
                    <i class="fa-solid fa-code"></i>
                    Swagger Docs
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-4xl w-full mx-auto px-4 py-12 flex flex-col items-center">
        <!-- Hero Section -->
        <div class="text-center mb-10 space-y-3">
            <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Free File Conversions
            </h1>
            <p class="text-slate-400 text-sm sm:text-base max-w-lg mx-auto">
                Stateless, 100% private, and fast. Files are processed in memory and never stored on our servers.
            </p>
        </div>

        <!-- Tool Selection Tabs -->
        <div class="w-full grid grid-cols-2 sm:grid-cols-4 gap-2 p-1.5 bg-slate-900/90 rounded-2xl border border-slate-800 mb-8 shadow-xl">
            <button onclick="setTool('pdf-to-docx')" id="tab-pdf-to-docx" class="tool-tab active flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-xs sm:text-sm font-medium transition duration-150">
                <i class="fa-regular fa-file-pdf text-rose-400"></i>
                PDF to Word
            </button>
            <button onclick="setTool('docx-to-pdf')" id="tab-docx-to-pdf" class="tool-tab flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-xs sm:text-sm font-medium transition duration-150">
                <i class="fa-regular fa-file-word text-blue-400"></i>
                Word to PDF
            </button>
            <button onclick="setTool('images-to-pdf')" id="tab-images-to-pdf" class="tool-tab flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-xs sm:text-sm font-medium transition duration-150">
                <i class="fa-regular fa-images text-emerald-400"></i>
                Images to PDF
            </button>
            <button onclick="setTool('pdf-to-images')" id="tab-pdf-to-images" class="tool-tab flex items-center justify-center gap-2 py-3 px-4 rounded-xl text-xs sm:text-sm font-medium transition duration-150">
                <i class="fa-solid fa-photo-film text-amber-400"></i>
                PDF to Images
            </button>
        </div>

        <!-- Dropzone Card -->
        <div class="w-full bg-slate-900/40 rounded-3xl border border-slate-800/80 p-8 shadow-2xl backdrop-blur">
            <div id="dropzone" class="border-2 border-dashed border-slate-700 hover:border-indigo-500 hover:bg-indigo-950/10 transition-all duration-200 rounded-2xl p-10 flex flex-col items-center justify-center text-center cursor-pointer group">
                <input type="file" id="fileInput" class="hidden" onchange="handleFileSelect(event)">
                
                <div id="dropzoneIcon" class="w-16 h-16 mb-4 rounded-2xl bg-slate-800/80 group-hover:bg-indigo-600/20 group-hover:scale-110 flex items-center justify-center transition-all duration-200 text-slate-400 group-hover:text-indigo-400">
                    <i class="fa-solid fa-cloud-arrow-up text-2xl"></i>
                </div>
                
                <p class="font-semibold text-slate-200 text-base mb-1" id="dropzonePrompt">
                    Drag and drop your file here, or <span class="text-indigo-400 underline">browse</span>
                </p>
                <p class="text-xs text-slate-500" id="dropzoneHint">Supported: .pdf (Max 50MB)</p>
            </div>

            <!-- Selected File Preview -->
            <div id="filePreview" class="hidden mt-6 p-4 rounded-xl bg-slate-800/50 border border-slate-700/60 flex items-center justify-between">
                <div class="flex items-center gap-3 overflow-hidden">
                    <div class="w-10 h-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-lg shrink-0">
                        <i class="fa-regular fa-file" id="fileIcon"></i>
                    </div>
                    <div class="truncate">
                        <p class="font-medium text-sm text-slate-200 truncate" id="fileName">document.pdf</p>
                        <p class="text-xs text-slate-400" id="fileSize">1.2 MB</p>
                    </div>
                </div>
                <button onclick="clearFile()" class="p-2 text-slate-400 hover:text-rose-400 transition">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <!-- Action Button & Status -->
            <div class="mt-6 flex flex-col gap-3">
                <button id="convertBtn" onclick="startConversion()" disabled class="w-full py-4 rounded-xl font-semibold text-sm bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed transition duration-150 flex items-center justify-center gap-2 shadow-lg shadow-indigo-600/25">
                    <i class="fa-solid fa-arrows-rotate" id="btnIcon"></i>
                    <span id="btnText">Convert Now</span>
                </button>

                <!-- Status Banner -->
                <div id="statusAlert" class="hidden p-4 rounded-xl text-sm flex items-center gap-3">
                    <i id="statusIcon" class="text-base"></i>
                    <span id="statusMessage"></span>
                </div>
            </div>
        </div>

        <!-- Privacy & Security Notice -->
        <div class="mt-8 flex items-center gap-2 text-xs text-slate-500">
            <i class="fa-solid fa-shield-halved text-emerald-500"></i>
            <span>Zero Data Retention: Files are permanently purged immediately after download.</span>
        </div>
    </main>

    <footer class="border-t border-slate-800/60 py-6 text-center text-xs text-slate-600">
        FreeShits &bull; Free File Conversions & Image Tools
    </footer>

    <script>
        let currentTool = 'pdf-to-docx';
        let selectedFiles = [];

        const toolConfig = {
            'pdf-to-docx': {
                endpoint: '/api/convert/pdf-to-docx',
                accept: '.pdf',
                multiple: false,
                hint: 'Supported: .pdf (Max 50MB)',
                outName: (n) => n.replace(/\\.[^/.]+$/, "") + ".docx"
            },
            'docx-to-pdf': {
                endpoint: '/api/convert/docx-to-pdf',
                accept: '.docx,.doc',
                multiple: false,
                hint: 'Supported: .docx, .doc (Max 50MB)',
                outName: (n) => n.replace(/\\.[^/.]+$/, "") + ".pdf"
            },
            'images-to-pdf': {
                endpoint: '/api/convert/images-to-pdf',
                accept: '.png,.jpg,.jpeg,.webp',
                multiple: true,
                hint: 'Supported: .png, .jpg, .webp (Select single or multiple)',
                outName: () => "converted_images.pdf"
            },
            'pdf-to-images': {
                endpoint: '/api/convert/pdf-to-images',
                accept: '.pdf',
                multiple: false,
                hint: 'Supported: .pdf (Extracts 200 DPI PNGs or ZIP)',
                outName: (n) => n.replace(/\\.[^/.]+$/, "") + "_pages.zip"
            }
        };

        function setTool(tool) {
            currentTool = tool;
            document.querySelectorAll('.tool-tab').forEach(b => {
                b.classList.remove('bg-indigo-600', 'text-white', 'shadow-md');
                b.classList.add('text-slate-400', 'hover:text-slate-200');
            });
            const activeBtn = document.getElementById('tab-' + tool);
            activeBtn.classList.add('bg-indigo-600', 'text-white', 'shadow-md');
            activeBtn.classList.remove('text-slate-400');

            const cfg = toolConfig[tool];
            const fileInput = document.getElementById('fileInput');
            fileInput.accept = cfg.accept;
            fileInput.multiple = cfg.multiple;
            document.getElementById('dropzoneHint').innerText = cfg.hint;
            clearFile();
        }

        // Initialize active tab styling
        setTool('pdf-to-docx');

        // Drag & Drop
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('fileInput');

        dropzone.addEventListener('click', () => fileInput.click());
        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('border-indigo-500', 'bg-indigo-950/20');
        });
        dropzone.addEventListener('dragleave', () => {
            dropzone.classList.remove('border-indigo-500', 'bg-indigo-950/20');
        });
        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('border-indigo-500', 'bg-indigo-950/20');
            if (e.dataTransfer.files.length > 0) {
                processFiles(e.dataTransfer.files);
            }
        });

        function handleFileSelect(event) {
            if (event.target.files.length > 0) {
                processFiles(event.target.files);
            }
        }

        function processFiles(files) {
            selectedFiles = Array.from(files);
            if (selectedFiles.length === 0) return;

            const preview = document.getElementById('filePreview');
            const fileName = document.getElementById('fileName');
            const fileSize = document.getElementById('fileSize');
            const convertBtn = document.getElementById('convertBtn');

            if (selectedFiles.length === 1) {
                fileName.innerText = selectedFiles[0].name;
                fileSize.innerText = (selectedFiles[0].size / (1024 * 1024)).toFixed(2) + ' MB';
            } else {
                fileName.innerText = `${selectedFiles.length} images selected`;
                const total = selectedFiles.reduce((acc, f) => acc + f.size, 0);
                fileSize.innerText = (total / (1024 * 1024)).toFixed(2) + ' MB total';
            }

            preview.classList.remove('hidden');
            convertBtn.disabled = false;
            hideStatus();
        }

        function clearFile() {
            selectedFiles = [];
            fileInput.value = '';
            document.getElementById('filePreview').classList.add('hidden');
            document.getElementById('convertBtn').disabled = true;
            hideStatus();
        }

        function showStatus(type, message) {
            const alert = document.getElementById('statusAlert');
            const icon = document.getElementById('statusIcon');
            const msg = document.getElementById('statusMessage');

            alert.className = 'p-4 rounded-xl text-sm flex items-center gap-3 ';
            if (type === 'error') {
                alert.classList.add('bg-rose-950/60', 'text-rose-300', 'border', 'border-rose-800');
                icon.className = 'fa-solid fa-triangle-exclamation text-rose-400';
            } else if (type === 'success') {
                alert.classList.add('bg-emerald-950/60', 'text-emerald-300', 'border', 'border-emerald-800');
                icon.className = 'fa-solid fa-circle-check text-emerald-400';
            } else {
                alert.classList.add('bg-indigo-950/60', 'text-indigo-300', 'border', 'border-indigo-800');
                icon.className = 'fa-solid fa-spinner fa-spin text-indigo-400';
            }

            msg.innerText = message;
            alert.classList.remove('hidden');
        }

        function hideStatus() {
            document.getElementById('statusAlert').classList.add('hidden');
        }

        async function startConversion() {
            if (selectedFiles.length === 0) return;

            const cfg = toolConfig[currentTool];
            const btn = document.getElementById('convertBtn');
            const btnText = document.getElementById('btnText');
            const btnIcon = document.getElementById('btnIcon');

            btn.disabled = true;
            btnIcon.className = 'fa-solid fa-spinner fa-spin';
            btnText.innerText = 'Converting...';
            showStatus('info', 'Processing file conversion on server...');

            const formData = new FormData();
            if (cfg.multiple) {
                selectedFiles.forEach(f => formData.append('files', f));
            } else {
                formData.append('file', selectedFiles[0]);
            }

            try {
                const response = await fetch(cfg.endpoint, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const err = await response.json().catch(() => ({ detail: 'Conversion failed' }));
                    throw new Error(err.detail || 'Error during conversion');
                }

                // Trigger file download
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                
                // Get filename from response or fallback
                let downloadName = cfg.outName(selectedFiles[0].name);
                const disposition = response.headers.get('Content-Disposition');
                if (disposition && disposition.indexOf('filename=') !== -1) {
                    const matches = /filename[^;=\\n]*=((['"]).*?\\2|[^;\\n]*)/.exec(disposition);
                    if (matches && matches[1]) downloadName = matches[1].replace(/['"]/g, '');
                }

                a.download = downloadName;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);

                showStatus('success', `Success! Downloaded: ${downloadName}`);
            } catch (err) {
                showStatus('error', err.message);
            } finally {
                btn.disabled = false;
                btnIcon.className = 'fa-solid fa-arrows-rotate';
                btnText.innerText = 'Convert Now';
            }
        }
    </script>
</body>
</html>"""
