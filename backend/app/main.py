from fastapi import FastAPI, HTTPException, status, Depends
from app.api.v1.routes import subscribe
from app.api.v1.routes import admin
from app.api.v1.routes import spotify_search
from fastapi.middleware.cors import CORSMiddleware
from app.db.beanie_db import init_database, test_connection, get_database
from app.middleware.error_handler import ErrorHandler
from app.middleware.http_middleware import error_handling_middleware
from app.models.beanie_models import User, Notification
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



@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    try:
        # Initialize Beanie database
        success = await init_database()
        if success:
            logging.info("Beanie database initialized successfully")
        else:
            logging.warning("Database initialization failed, but app will continue")
    except Exception as e:
        logging.error(f"Startup error: {e}")
        # Don't raise here to allow the app to start even if DB is down


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    try:
        from app.db.beanie_db import close_connection
        await close_connection()
        logging.info("Database connection closed")
    except Exception as e:
        logging.error(f"Shutdown error: {e}")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint with database connectivity test"""
    try:
        # Test database connection
        is_connected = await test_connection()
        if is_connected:
            return {"status": "ok", "database": "connected"}
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection failed"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {e}"
        )


@app.get("/test/db")
async def test_database():
    """Test endpoint to verify database operations"""
    try:
        # Test a simple database operation with Beanie
        user_count = await User.count()
        
        return {
            "status": "ok",
            "message": "Database operations working",
            "user_count": user_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database test error: {e}"
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Music Release Notifier API",
        "status": "running",
        "version": "1.0.0"
    }
