# app/main.py
"""
FastAPI Application Entry Point for Address Book API.
Includes:
- Database table creation
- Router registration
- Logging middleware
- Global exception handling
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import engine
from app.models.address import Address
from app.routes.addressRoute import router  # assume routes/address.py and router inside
from app.logging_config import logger

# -------------------------
# Create DB tables
# -------------------------
# This ensures all tables defined via SQLAlchemy models exist in DB
Address.metadata.create_all(bind=engine)

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="Address Book API", version="1.0")

# -------------------------
# Include Routers
# -------------------------
app.include_router(router)  # singular router name for clarity

# -------------------------
# Middleware: Logging
# -------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Logs every incoming request and outgoing response.
    """
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Completed request: {request.method} {request.url} - Status {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Unhandled exception during request: {request.method} {request.url} - {e}")
        raise e  # propagate exception to global handler

# -------------------------
# Global Exception Handler
# -------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handles all uncaught exceptions and returns a 500 JSON response.
    """
    logger.error(f"Unhandled exception: {exc} - Path: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )