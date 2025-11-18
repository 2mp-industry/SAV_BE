from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logger import app_logger
from core.middleware import logging_middleware
from routers import job, user
from db.database import create_tables

try:
    create_tables()
except Exception as e:
    app_logger.error(f"Database initialization failed: {e}")
    raise

app = FastAPI(
    title="Service après vente",
    description="Description Service Après vente",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.middleware("http")(logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)

@app.on_event("startup")
async def startup_event():
    app_logger.info("App API starting up")

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("App API shutting down")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "App-api"}

if __name__ == "__main__":
    import uvicorn
    app_logger.info("Starting uvicorn server on localhost:8000")
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, access_log=False )
        
        
        
       