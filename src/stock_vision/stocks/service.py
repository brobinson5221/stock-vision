from stock_vision.stocks.schemas import PageQuery, StockDataset, StockPage


def _in_range(value: float | None, lower: float | None, upper: float | None) -> bool:
    if lower is None and upper is None:
        return True
    return (
        value is not None
        and (lower is None or value >= lower)
        and (upper is None or value <= upper)
    )


def browse_stocks(source: StockDataset, page: PageQuery) -> StockPage:
    """Filter and sort before slicing the matching stocks."""
    search = page.q.strip().casefold()
    sector = page.sector.strip().casefold()
    matches = (
        stock
        for stock in source.items
        if (not sector or stock.sector.casefold() == sector)
        and (search in stock.symbol.casefold() or search in stock.name.casefold())
        and _in_range(stock.price, page.min_price, page.max_price)
        and _in_range(stock.market_cap, page.min_market_cap, page.max_market_cap)
        and _in_range(stock.pe_ratio, page.min_pe_ratio, page.max_pe_ratio)
    )
    ordered = sorted(matches, key=lambda stock: stock.symbol)
    if page.sort_by != "symbol" or page.sort_dir == "desc":
        descending = page.sort_dir == "desc"

        def sort_key(stock):
            value = getattr(stock, page.sort_by)
            # Reverse the null rank with the sort direction so nulls always come last.
            null_rank = (value is not None) if descending else (value is None)
            return (null_rank, value)

        # Python's stable sort preserves ascending symbol order for equal keys.
        ordered.sort(key=sort_key, reverse=descending)
    return StockPage(
        items=tuple(ordered[page.offset : page.offset + page.limit]),
        total=len(ordered),
        limit=page.limit,
        offset=page.offset,
        provenance=source.provenance,
        currency=source.currency,
    )
