# ruff: noqa: INP001 -- Test server runs as a standalone script.
import uvicorn

from stock_vision.main import app
from stock_vision.stocks.schemas import StockDataset
from stock_vision.stocks.source import load_sample_stocks


def paginated_sample() -> StockDataset:
    sample = load_sample_stocks()
    # Extend the six packaged rows past the browser's 50-row page boundary.
    extra = tuple(
        sample.items[0].model_copy(update={"symbol": f"TEST{index:02d}"}) for index in range(1, 46)
    )
    return StockDataset(items=sample.items + extra)


if __name__ == "__main__":
    app.dependency_overrides[load_sample_stocks] = paginated_sample
    uvicorn.run(app, host="127.0.0.1", port=8000)
