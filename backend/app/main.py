from fastapi import FastAPI
app = FastAPI()

app = FastAPI(
    title = "ATS Resume Scanner",
    description = "This is a the API for the ATS Resume Scanner application",
    version = "0.1.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Taloring Engine!",
            "status": "running"}
@app.get("/health")
def health():
    return {"message": "API is healthy and running",
            "status": "healthy"}
