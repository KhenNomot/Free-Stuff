from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import router as conversion_router

# Path to decoupled frontend assets
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

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

# Mount decoupled frontend assets (CSS, JS)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FreeShits Conversion Engine",
        "privacy": "Zero-Retention / Ephemeral"
    }

@app.get("/")
def home():
    return FileResponse(str(FRONTEND_DIR / "index.html"))
