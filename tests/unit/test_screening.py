# ruff: noqa: INP001, S101 -- Pytest tests outside the installed package.
from stock_vision.stocks.schemas import PageQuery, StockDataset
from stock_vision.stocks.service import browse_stocks
from stock_vision.stocks.source import load_sample_stocks


def test_ordering_precedes_pagination_without_mutating_source():
    source = StockDataset(items=tuple(reversed(load_sample_stocks().items)))
    original = source.items
    first = browse_stocks(source, PageQuery(limit=2))
    second = browse_stocks(source, PageQuery(limit=2, offset=2))
    assert [stock.symbol for stock in first.items + second.items] == [
        "DEMOA",
        "DEMOB",
        "DEMOC",
        "DEMOD",
    ]
    assert first.total == len(original)
    assert source.items == original
    assert first.provenance == source.provenance
    assert first.currency == source.currency


def test_empty_and_out_of_range_pages():
    empty = browse_stocks(StockDataset(items=()), PageQuery())
    assert empty.items == ()
    assert empty.total == 0
    page = browse_stocks(load_sample_stocks(), PageQuery(offset=100))
    assert page.items == ()
    assert page.total == len(load_sample_stocks().items)


def test_filtering_precedes_pagination():
    source = StockDataset(items=tuple(reversed(load_sample_stocks().items)))
    page = browse_stocks(source, PageQuery(q=" demo ", sector=" teCHNOLOGY ", limit=1, offset=1))
    assert [stock.symbol for stock in page.items] == ["DEMOD"]
    assert page.total == 2  # noqa: PLR2004 -- Two Technology rows match.
