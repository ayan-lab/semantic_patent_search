from fastapi import FastAPI
from routes import search_routes

app = FastAPI(title="Tech Documents Search")

app.include_router(search_routes.router, prefix="/search", tags=["search"])

@app.get("/")
def root():
    return {"status": 'Working !!'}
