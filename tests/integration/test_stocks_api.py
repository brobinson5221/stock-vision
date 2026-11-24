# ruff: noqa: INP001, S101, PLR2004 -- HTTP contract assertions in pytest.
import pytest
from fastapi.testclient import TestClient

from stock_vision.main import app
from stock_vision.stocks.schemas import StockDataset
from stock_vision.stocks.source import load_sample_stocks


@pytest.fixture
def dataset():
    template = load_sample_stocks().items[0]
    return StockDataset(
        items=tuple(
            template.model_copy(update={"symbol": f"ROW{index:03}"})
            for index in reversed(range(105))
        ),
    )


@pytest.fixture
def client(monkeypatch, dataset):
    monkeypatch.setitem(app.dependency_overrides, load_sample_stocks, lambda: dataset)
    with TestClient(app) as test_client:
        yield test_client


def test_health_and_default_sample():
    with TestClient(app) as client:
        assert client.get("/api/health").json() == {"status": "ok"}
        response = client.get("/api/stocks")
    assert response.status_code == 200
    data = response.json()
    assert data["provenance"] == "synthetic-sample"
    assert data["currency"] == "USD"
    assert data["limit"] == 50
    assert data["offset"] == 0
    assert data["total"] == 6
    assert any(stock["pe_ratio"] is None for stock in data["items"])


def test_multiple_pages_use_overridden_source(client, dataset):
    original = dataset.items
    rows = []
    for offset in (0, 50, 100):
        response = client.get("/api/stocks", params={"offset": offset})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 105
        assert data["offset"] == offset
        rows.extend(stock["symbol"] for stock in data["items"])
    assert rows == [f"ROW{index:03}" for index in range(105)]
    assert dataset.items == original
    assert len(client.get("/api/stocks?limit=100").json()["items"]) == 100


@pytest.mark.parametrize(
    "query",
    [
        "limit=0",
        "limit=-1",
        "limit=101",
        "limit=nope",
        "limit=1.5",
        "offset=-1",
        "offset=nope",
        "offset=1.5",
        "limit=nan",
        "offset=inf",
    ],
)
def test_invalid_page_queries_return_validation_errors(client, query):
    response = client.get(f"/api/stocks?{query}")
    assert response.status_code == 422
    assert response.json()["detail"]


def test_out_of_range_page_keeps_total(client):
    response = client.get("/api/stocks?offset=105")
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 105


@pytest.mark.parametrize(
    ("params", "symbols"),
    [
        ({"q": "moB"}, ["DEMOB"]),
        ({"q": "aLPha", "sector": "TECHNOLOGY"}, ["DEMOA"]),
        ({"q": "Alpha", "sector": "Energy"}, []),
        ({"q": " ", "sector": " "}, ["DEMOA", "DEMOB", "DEMOC", "DEMOD", "DEMOE", "DEMOF"]),
        ({"sector": "Health"}, []),
    ],
)
def test_stock_search_and_sector_filters(params, symbols):
    with TestClient(app) as client:
        response = client.get("/api/stocks", params=params)
    assert response.status_code == 200
    data = response.json()
    assert [stock["symbol"] for stock in data["items"]] == symbols
    assert data["total"] == len(symbols)


@pytest.mark.parametrize("field", ["q", "sector"])
def test_overlong_stock_filters_are_rejected(client, field):
    response = client.get("/api/stocks", params={field: "x" * 101})
    assert response.status_code == 422


def test_empty_source(monkeypatch):
    monkeypatch.setitem(
        app.dependency_overrides,
        load_sample_stocks,
        lambda: StockDataset(items=()),
    )
    with TestClient(app) as client:
        data = client.get("/api/stocks").json()
    assert data["items"] == []
    assert data["total"] == 0
