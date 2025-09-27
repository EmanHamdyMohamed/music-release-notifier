from app.core.spotify_client import SpotifyClient
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
    # Schedule check_new_releases_and_notify to run every 1 hour
    scheduler.add_job(check_new_releases_and_notify, "interval", hours=1)
    scheduler.start()


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    try:
        # Test database connection with ping command
        await client.admin.command('ping')
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB connection failed: {e}"
        )
