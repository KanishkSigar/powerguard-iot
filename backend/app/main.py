"""
PowerGuard IoT — Main Application Entry Point

FastAPI application with MQTT subscriber, InfluxDB integration,
and REST API endpoints.
"""

import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router
from app.mqtt_service import mqtt_service
from app.database import db

# ----------------------
# Logging Configuration
# ----------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ----------------------
# Application Lifespan
# ----------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info("=" * 50)
    logger.info("  PowerGuard IoT — Backend Server Starting")
    logger.info("=" * 50)

    # Start MQTT subscriber
    loop = asyncio.get_running_loop()
    mqtt_service.start(loop=loop)
    logger.info("MQTT subscriber started.")

    yield

    # Shutdown
    logger.info("Shutting down services...")
    mqtt_service.stop()
    db.close()
    logger.info("All services stopped. Goodbye!")


# ----------------------
# FastAPI Application
# ----------------------

app = FastAPI(
    title="PowerGuard IoT API",
    description="Smart Energy Meter with Anomaly Detection — REST API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ----------------------
# CORS Middleware
# ----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Include API Routes
# ----------------------

app.include_router(router)


# ----------------------
# Health Check
# ----------------------

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "powerguard-iot-backend",
        "version": "1.0.0",
    }


# ----------------------
# Run with Uvicorn
# ----------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info",
    )
