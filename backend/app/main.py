from app.core.spotify_client import SpotifyClient
from app.core.config import settings
from fastapi import FastAPI, HTTPException, status
from app.api.v1.routes import subscribe
from app.services.notifier import check_new_releases_and_notify
from app.utils.scheduler import scheduler
from app.api.v1.routes import admin
from app.api.v1.routes import spotify_search
from fastapi.middleware.cors import CORSMiddleware
from app.db.mongo import client
from app.middleware.error_handler import ErrorHandler
from app.middleware.http_middleware import error_handling_middleware
import asyncio
import logging


app = FastAPI(title="Music Release Notifier")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add HTTP middleware
app.middleware("http")(error_handling_middleware)

# Add error handlers
app.add_exception_handler(HTTPException, ErrorHandler.handle_http_exception)
app.add_exception_handler(ValueError, ErrorHandler.handle_value_error)
app.add_exception_handler(ConnectionError, ErrorHandler.handle_connection_error)
app.add_exception_handler(TimeoutError, ErrorHandler.handle_timeout_error)


app.include_router(subscribe.router, prefix="/api/v1")
app.include_router(spotify_search.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1/admin")

spotify_client = SpotifyClient()


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    try:
        # Test database connection
        await client.admin.command('ping')
        logging.info("Database connection established successfully")
        
        # Schedule check_new_releases_and_notify to run every 1 hour
        scheduler.add_job(check_new_releases_and_notify, "interval", hours=1)
        scheduler.start()
        logging.info("Scheduler started successfully")
        
    except Exception as e:
        logging.error(f"Startup error: {e}")
        # Don't raise here to allow the app to start even if DB is down


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    try:
        # Stop scheduler
        if scheduler.running:
            scheduler.shutdown()
            logging.info("Scheduler stopped")
        
        # Close database connection
        client.close()
        logging.info("Database connection closed")
        
    except Exception as e:
        logging.error(f"Shutdown error: {e}")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    try:
        # Test database connection with ping command
        await asyncio.wait_for(
            client.admin.command('ping'),
            timeout=5.0
        )
        return {"status": "ok", "database": "connected"}
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB connection timeout"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB connection failed: {e}"
        )


@app.get("/test/db")
async def test_database():
    """Test endpoint to verify database operations"""
    try:
        from app.db.mongo import db
        
        # Test a simple database operation
        result = await db.users.find_one({"email": "test@example.com"})
        
        return {
            "status": "ok",
            "message": "Database operations working",
            "result": result is not None
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database test error: {e}"
        )
