from importlib.resources import files

from stock_vision.stocks.schemas import StockDataset


def load_sample_stocks() -> StockDataset:
    """Load immutable synthetic stocks; propagate resource and validation errors."""
    resource = files("stock_vision.stocks").joinpath("sample_stocks.json")
    return StockDataset.model_validate_json(resource.read_text(encoding="utf-8"))
