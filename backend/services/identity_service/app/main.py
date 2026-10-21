
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.auth import router as auth_router

app = FastAPI(
    title="LeadFlow Identity API",
    description="Authentication and user management service",
    version="1.0.0"
)

# Development-only frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

app.include_router(health_router)
app.include_router(auth_router)
