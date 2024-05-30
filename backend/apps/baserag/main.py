from fastapi import FastAPI
from .routers import document_router,search_router

app = FastAPI()

app.include_router(document_router.router, prefix="/document", tags=["document"])
app.include_router(search_router.router, prefix="/search", tags=["search"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Baserag API!"}

