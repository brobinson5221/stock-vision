# ruff: noqa: INP001, S101, PLR2004 -- HTTP contract assertions in pytest.
import pytest
from fastapi.testclient import TestClient

from stock_vision.main import app, create_app
from stock_vision.stocks.schemas import StockDataset
from stock_vision.stocks.source import load_sample_stocks


def test_served_frontend_keeps_api_errors_json(tmp_path):
    assets = tmp_path / "assets"
    assets.mkdir()
    (tmp_path / "index.html").write_text('<script src="/assets/app.js"></script>', encoding="utf-8")
    (assets / "app.js").write_text('fetch("/api/stocks");', encoding="utf-8")

    with TestClient(create_app(tmp_path)) as client:
        assert client.get("/").headers["content-type"].startswith("text/html")
        assert client.get("/assets/app.js").text == 'fetch("/api/stocks");'
        assert client.get("/api/health").json() == {"status": "ok"}
        missing = client.get("/api/missing")
        assert missing.status_code == 404
        assert missing.json() == {"detail": "Not Found"}
        invalid = client.get("/api/stocks?limit=0")
        assert invalid.status_code == 422
        assert invalid.json()["detail"]


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
    assert data["source_name"] == "Synthetic sample data"
    assert data["as_of"] is None
    assert data["sectors"] == ["Energy", "Healthcare", "Industrials", "Technology"]
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


@pytest.mark.parametrize(
    ("query", "symbols", "total"),
    [
        ("min_price=25&max_price=25", ["DEMOC"], 1),
        ("min_market_cap=0", ["DEMOA", "DEMOB", "DEMOD", "DEMOE", "DEMOF"], 5),
        ("max_pe_ratio=25", ["DEMOA", "DEMOC", "DEMOD", "DEMOE", "DEMOF"], 5),
        ("max_pe_ratio=-1", [], 0),
        (
            (
                "q=demo&sector=Technology&max_price=75&max_market_cap=1000000000"
                "&min_pe_ratio=25&max_pe_ratio=25&limit=1"
            ),
            ["DEMOD"],
            1,
        ),
        ("min_price=75&limit=1&offset=1", ["DEMOD"], 2),
    ],
)
def test_stock_financial_ranges(query, symbols, total):
    with TestClient(app) as client:
        response = client.get(f"/api/stocks?{query}")
    assert response.status_code == 200
    data = response.json()
    assert [stock["symbol"] for stock in data["items"]] == symbols
    assert data["total"] == total


@pytest.mark.parametrize(
    "query",
    [
        "min_price=100&max_price=75",
        "min_market_cap=2&max_market_cap=1",
        "min_pe_ratio=-1&max_pe_ratio=-2",
        "min_price=",
        "max_price=abc",
        "min_market_cap=-1",
        "max_price=-1",
        "min_price=inf",
        "max_market_cap=1e999",
        "min_pe_ratio=nan",
    ],
)
def test_invalid_stock_ranges_return_validation_errors(client, query):
    response = client.get(f"/api/stocks?{query}")
    assert response.status_code == 422
    assert response.json()["detail"]


@pytest.mark.parametrize(
    ("query", "symbols"),
    [
        ("sort_by=price&sort_dir=asc&q=demo&sector=Technology&min_price=75", ["DEMOD", "DEMOA"]),
        ("sort_by=market_cap&sort_dir=asc", ["DEMOE", "DEMOF", "DEMOB", "DEMOD", "DEMOA", "DEMOC"]),
        (
            "sort_by=market_cap&sort_dir=desc",
            ["DEMOA", "DEMOD", "DEMOB", "DEMOF", "DEMOE", "DEMOC"],
        ),
        ("sort_by=pe_ratio&sort_dir=desc", ["DEMOA", "DEMOD", "DEMOF", "DEMOC", "DEMOE", "DEMOB"]),
        ("sort_by=sector&sort_dir=asc", ["DEMOE", "DEMOB", "DEMOF", "DEMOC", "DEMOA", "DEMOD"]),
        ("sort_by=name&sort_dir=desc", ["DEMOF", "DEMOC", "DEMOE", "DEMOD", "DEMOB", "DEMOA"]),
        ("sort_by=symbol&sort_dir=desc", ["DEMOF", "DEMOE", "DEMOD", "DEMOC", "DEMOB", "DEMOA"]),
    ],
)
def test_stock_sorting(query, symbols):
    with TestClient(app) as client:
        response = client.get(f"/api/stocks?{query}")
    assert response.status_code == 200
    data = response.json()
    assert [stock["symbol"] for stock in data["items"]] == symbols
    assert data["total"] == len(symbols)


@pytest.mark.parametrize("query", ["sort_by=unknown", "sort_dir=down"])
def test_invalid_stock_sort_returns_validation_error(client, query):
    response = client.get(f"/api/stocks?{query}")
    assert response.status_code == 422
    assert response.json()["detail"]


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
