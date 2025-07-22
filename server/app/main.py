from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
import os

app = FastAPI(
 title="Renewable Energy Investment Analyzer",
 description="AI-powered solar panel investment feasibility analyzer for Germany",
 version="1.0.0"
)

# CORS configuration - allows both local development and production
ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:3000",
    "https://renewable-analyzer.vercel.app",
    "https://renewable-analyzer-fawphiwxq-muhammadusman876s-projects.vercel.app",
    "*"  # Temporary: allow all origins for debugging
]

# Add custom origins from environment variable if provided
custom_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if custom_origins and custom_origins[0]:  # Check if not empty
    ALLOWED_ORIGINS.extend([origin.strip() for origin in custom_origins])

print(f"🔧 CORS Debug: Allowed origins = {ALLOWED_ORIGINS}")

# CORS middleware for frontend communication
app.add_middleware(
 CORSMiddleware,
 allow_origins=ALLOWED_ORIGINS,
 allow_credentials=True,
 allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
 allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
 return {
 "message": "Renewable Energy Investment Analyzer API",
 "version": "1.0.0",
 "docs": "/docs"
 }

@app.get("/health")
async def health():
 return {"status": "healthy", "service": "renewable-analyzer-api"}

@app.get("/cors-test")
async def cors_test():
 return {"message": "CORS is working!", "origins": ALLOWED_ORIGINS}

if __name__ == "__main__":
 import uvicorn
 uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)
