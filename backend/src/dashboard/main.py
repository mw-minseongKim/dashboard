from fastapi import FastAPI

from dashboard.api import router

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"message": "health check"}


app.include_router(router=router)
