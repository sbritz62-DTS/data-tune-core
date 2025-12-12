"""
Time Tracking App - FastAPI Backend
Serves REST API and static frontend
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Time Tracking App",
    description="Track time, manage clients, generate invoices",
    version="2.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from app.routes import clients, timesheet, invoices

# Include routers
app.include_router(clients.router, prefix="/api", tags=["clients"])
app.include_router(timesheet.router, prefix="/api", tags=["timesheet"])
app.include_router(invoices.router, prefix="/api", tags=["invoices"])

# Mount static files
frontend_path = Path(__file__).parent.parent / "frontend"
if (frontend_path / "static").exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

# Serve index.html for all routes (SPA)
@app.get("/")
async def root():
    """Serve main page"""
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Time Tracking App API"}

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    """Catch all routes and serve index.html for SPA routing"""
    index_path = frontend_path / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Path not found"}

# Health check
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import webbrowser
    import uvicorn
    import threading
    import time
    
    logger.info("Starting Time Tracking App...")
    
    def run_server():
        """Run the server"""
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start, then open browser
    time.sleep(2)
    logger.info("Opening browser to http://127.0.0.1:8000")
    webbrowser.open("http://127.0.0.1:8000")
    
    # Keep main thread alive
    try:
        server_thread.join()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
