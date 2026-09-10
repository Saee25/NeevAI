from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import generate

app = FastAPI(title="AI Co-Founder API")

app.include_router(generate.router)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def hello_world():
    return {"message": "Hello from AI Co-Founder Backend!"}
