from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from routes.auth import router as auth_router
from routes.events import router as events_router

app = FastAPI(title="Event Announcement API")

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:80",
    "http://frontend",
    "http://frontend:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(events_router, prefix="/events", tags=["Events"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Event Announcement API"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 