from app.core.spotify_client import SpotifyClient
from fastapi import FastAPI
from app.api.v1.routes import subscribe
from app.services.notifier import check_new_releases_and_notify
from app.utils.scheduler import scheduler
from app.api.v1.routes import admin
from app.api.v1.routes import spotify_search 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Music Release Notifier")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.js dev server default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscribe.router, prefix="/api/v1")
app.include_router(spotify_search.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1/admin")

spotify_client = SpotifyClient()

# @app.get("/api/v1/new-releases")
# async def get_new_releases():
#     data = await spotify_client.get_new_releases()
#     return data

# @app.get("/api/v1/check-notifications")
# async def check_notifications():
#     notifications = await check_new_releases_and_notify()
#     return notifications


@app.on_event("startup")
async def startup_event():
    # Schedule check_new_releases_and_notify to run every 1 hour
    scheduler.add_job(check_new_releases_and_notify, "interval", hours=1)
    scheduler.start()
