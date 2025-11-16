"""Main FastAPI application for Arkatar World Studio."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    init_db()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(
    title="Arkatar World Studio API",
    description="API for managing fantasy world data",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "message": "Arkatar World Studio API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers
from .routes import locations, factions, characters, religions, items, relations, timeline, story_arcs, world

app.include_router(locations.router, prefix="/api")
app.include_router(factions.router, prefix="/api")
app.include_router(characters.router, prefix="/api")
app.include_router(religions.router, prefix="/api")
app.include_router(items.router, prefix="/api")
app.include_router(relations.router, prefix="/api")
app.include_router(timeline.router, prefix="/api")
app.include_router(story_arcs.router, prefix="/api")
app.include_router(world.router, prefix="/api")
