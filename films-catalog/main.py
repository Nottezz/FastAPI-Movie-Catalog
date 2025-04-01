from fastapi import FastAPI

app = FastAPI(
    title="Films",
    description="Films catalog",
    version="1.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}