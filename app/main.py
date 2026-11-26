
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for the CRM Platform",
    debug=settings.DEBUG,
)


@app.get("/")
def root():
    return {
        "message": "Welcome to CRM Platform API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
