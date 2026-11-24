from stock_vision.stocks.schemas import PageQuery, StockDataset, StockPage


def browse_stocks(source: StockDataset, page: PageQuery) -> StockPage:
    """Filter and order by symbol before slicing the matching stocks."""
    search = page.q.strip().casefold()
    sector = page.sector.strip().casefold()
    matches = (
        stock
        for stock in source.items
        if (not sector or stock.sector.casefold() == sector)
        and (search in stock.symbol.casefold() or search in stock.name.casefold())
    )
    ordered = sorted(matches, key=lambda stock: stock.symbol)
    return StockPage(
        items=tuple(ordered[page.offset : page.offset + page.limit]),
        total=len(ordered),
        limit=page.limit,
        offset=page.offset,
        provenance=source.provenance,
        currency=source.currency,
    )
