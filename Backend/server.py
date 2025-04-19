from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Base
from database import engine
from routes import api_router

app = FastAPI(title="ИдеяРелиз API", description="API for IdeaCodeRelease platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "IdeaRelease API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)