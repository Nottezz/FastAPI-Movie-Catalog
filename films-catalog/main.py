from fastapi import FastAPI, Request

app = FastAPI(
    title="Films",
    description="Films catalog",
    version="1.0",
)


@app.get("/")
def root(
    request: Request,
):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs_url": str(docs_url),
    }
