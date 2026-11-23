from stock_vision.stocks.schemas import PageQuery, StockDataset, StockPage


def browse_stocks(source: StockDataset, page: PageQuery) -> StockPage:
    """Order by symbol before slicing, leaving the source unchanged."""
    ordered = sorted(source.items, key=lambda stock: stock.symbol)
    return StockPage(
        items=tuple(ordered[page.offset : page.offset + page.limit]),
        total=len(ordered),
        limit=page.limit,
        offset=page.offset,
        provenance=source.provenance,
        currency=source.currency,
    )
