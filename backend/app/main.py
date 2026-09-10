from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import generate, validate
from app.middleware.rate_limit import limiter, custom_rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging

app = FastAPI(title="AI Co-Founder API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exceeded_handler)

app.include_router(generate.router)
app.include_router(validate.router)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://ai-cofounder.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc) or "An unexpected error occurred while communicating with the AI model."}
    )

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AI Co-Founder API is running"}

@app.get("/api/hello")
def hello_world():
    return {"message": "Hello from AI Co-Founder Backend!"}
