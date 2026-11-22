from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as conversion_router

app = FastAPI(
    title="FreeShits Conversion API",
    description="High-performance, stateless, zero-retention file conversion & image processing engine.",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app", "*"],
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
