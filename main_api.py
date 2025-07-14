import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

from src.api.routes import router

# Create FastAPI app
app = FastAPI(title="Restaurant Autocomplete API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Include router
app.include_router(router, prefix="/api")


# Redirect root to frontend
@app.get("/")
async def redirect_to_frontend():
    return RedirectResponse(url="/api/")


# Run the API with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
