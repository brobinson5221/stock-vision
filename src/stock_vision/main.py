from os import getenv
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from stock_vision.stocks.router import router


def health() -> dict[str, Literal["ok"]]:
    return {"status": "ok"}


def create_app(web_root: Path | None = None) -> FastAPI:
    app = FastAPI(title="Stock Vision", description="Synthetic sample data; not market quotes.")
    app.include_router(router)
    app.add_api_route("/api/health", health)

    if web_root is not None:
        index = web_root / "index.html"
        app.mount("/assets", StaticFiles(directory=web_root / "assets"), name="assets")

        @app.get("/", response_class=FileResponse, include_in_schema=False)
        def screener() -> FileResponse:
            return FileResponse(index, media_type="text/html")

    return app


web_root = getenv("STOCK_VISION_WEB_ROOT")
app = create_app(Path(web_root) if web_root else None)
