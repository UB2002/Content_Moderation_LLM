from fastapi import FastAPI
from routes.classificationRoutes import router
from config.db import Base, engine

app = FastAPI(debug=True)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

@app.get("/")
def index():
    return {"message": "Hello World"}