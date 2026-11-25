# ruff: noqa: INP001, S101 -- Pytest tests live outside the application package.
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from stock_vision.stocks import source
from stock_vision.stocks.schemas import PageQuery, Stock, StockDataset
from stock_vision.stocks.source import load_sample_stocks


def test_sample_source_is_valid_and_immutable():
    dataset = load_sample_stocks()
    assert dataset.provenance == "synthetic-sample"
    assert dataset.currency == "USD"
    assert dataset.items
    assert len({stock.symbol for stock in dataset.items}) == len(dataset.items)
    assert any(stock.pe_ratio is None for stock in dataset.items)
    assert any(stock.market_cap is None for stock in dataset.items)
    with pytest.raises(ValidationError, match="frozen"):
        dataset.items[0].price = 1


def test_concurrent_sample_loads_share_one_snapshot(monkeypatch):
    monkeypatch.setattr(source, "_sample_snapshot", None)
    resolve_resource = Mock(wraps=source.files)
    monkeypatch.setattr(source, "files", resolve_resource)

    with ThreadPoolExecutor(max_workers=4) as workers:
        snapshots = list(workers.map(lambda _: load_sample_stocks(), range(8)))

    assert all(snapshot is snapshots[0] for snapshot in snapshots)
    resolve_resource.assert_called_once_with("stock_vision.stocks")


def test_nullable_metrics_and_units():
    stock = Stock(
        symbol="DEMO",
        name="Demo",
        sector="Technology",
        price=10,
        market_cap=None,
        pe_ratio=None,
    )
    assert stock.market_cap is None
    assert stock.pe_ratio is None
    assert StockDataset(items=(stock,)).model_dump(mode="json")["currency"] == "USD"


@pytest.mark.parametrize(
    "changes",
    [
        {"symbol": ""},
        {"name": ""},
        {"name": "   "},
        {"sector": ""},
        {"price": -1},
        {"price": True},
        {"price": float("inf")},
        {"market_cap": -1},
        {"market_cap": float("nan")},
        {"pe_ratio": float("inf")},
        {"unexpected": 1},
    ],
)
def test_invalid_stocks_are_rejected(changes):
    values = {
        "symbol": "DEMO",
        "name": "Demo",
        "sector": "Technology",
        "price": 10,
        "market_cap": 1000,
        "pe_ratio": 12,
    }
    with pytest.raises(ValidationError):
        Stock(**(values | changes))


def test_page_defaults_and_boundaries():
    assert PageQuery().limit == 50  # noqa: PLR2004
    assert PageQuery().offset == 0
    assert PageQuery(limit=100, offset=10).limit == 100  # noqa: PLR2004


@pytest.mark.parametrize(
    "values",
    [
        {"limit": 0},
        {"limit": -1},
        {"limit": 101},
        {"offset": -1},
        {"limit": 1.5},
        {"limit": "invalid"},
    ],
)
def test_invalid_page_bounds_are_rejected(values):
    with pytest.raises(ValidationError):
        PageQuery(**values)


def test_source_rejects_invalid_resource(monkeypatch, tmp_path):
    monkeypatch.setattr(source, "_sample_snapshot", None)
    (tmp_path / "sample_stocks.json").write_text(
        '{"items": [{"symbol": "BROKEN"}]}',
        encoding="utf-8",
    )
    monkeypatch.setattr("stock_vision.stocks.source.files", lambda _package: tmp_path)
    with pytest.raises(ValidationError):
        load_sample_stocks()

    (tmp_path / "sample_stocks.json").write_text('{"items": []}', encoding="utf-8")
    assert load_sample_stocks().items == ()
