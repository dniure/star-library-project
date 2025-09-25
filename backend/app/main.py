from fastapi import FastAPI

app = FastAPI(title="STAR Library API")

@app.get("/")
def root():
    return {"message": "STAR Library API is running"}
