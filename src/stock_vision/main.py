from typing import Literal

from fastapi import FastAPI

from stock_vision.stocks.router import router

app = FastAPI(title="Stock Vision", description="Synthetic sample data; not market quotes.")
app.include_router(router)


@app.get("/api/health")
def health() -> dict[str, Literal["ok"]]:
    return {"status": "ok"}
