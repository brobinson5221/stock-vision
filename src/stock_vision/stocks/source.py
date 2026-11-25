from importlib.resources import files
from threading import Lock

from stock_vision.stocks.schemas import StockDataset

_sample_lock = Lock()
_sample_snapshot: StockDataset | None = None


def load_sample_stocks() -> StockDataset:
    """Load the packaged sample once per process after successful validation."""
    global _sample_snapshot  # noqa: PLW0603 -- Publish the process-local snapshot under the lock.
    with _sample_lock:
        if _sample_snapshot is None:
            resource = files("stock_vision.stocks").joinpath("sample_stocks.json")
            _sample_snapshot = StockDataset.model_validate_json(
                resource.read_text(encoding="utf-8"),
            )
        return _sample_snapshot
