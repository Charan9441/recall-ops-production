import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.incidents import router as incidents_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("recall_ops")

app = FastAPI(
    title="Recall-Ops Backend",
    description="Production Incident Intelligence powered by Persistent Hindsight Memory & Groq LLM",
    version="1.0.0",
)

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include incident routes
app.include_router(incidents_router, prefix="/api")
app.include_router(incidents_router)  # Direct root path support


@app.get("/")
async def root():
    return {
        "name": "Recall-Ops",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }
