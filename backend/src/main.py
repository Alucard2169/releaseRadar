from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import repo
from .database import Base, engine
import datetime
from datetime import timezone


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(repo.router, prefix="/repo", tags=["Repositories"])

@app.get("/")
async def root():
    return {
        "message": "Repository Dependency Security Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze-repository": "Analyze repository dependencies for security issues"
        },
        "authentication": {
            "github_token": "Optional - include as Bearer token for private repos and higher rate limits",
            "environment_variable": "GITHUB_TOKEN can be set as environment variable"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now(timezone.utc).isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)