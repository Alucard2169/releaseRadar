from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import repo
from .database import Base, engine

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
    return {"message": "GitHub Dependency Analyzer API running"}
