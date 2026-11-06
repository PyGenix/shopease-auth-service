from fastapi import FastAPI
from app.core.config import settings
from app.routers.auth_routes import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Independent ShopEase Authentication Microservice",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/", tags=["Service"])
def root():
    return {
        "service": settings.APP_NAME,
        "message": "Authentication microservice is running",
    }


@app.get("/health", tags=["Service"])
def health():
    return {
        "status": "healthy",
        "service": "authentication",
    }
