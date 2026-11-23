# ruff: noqa: TC001 -- FastAPI inspects model annotations at runtime.
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from stock_vision.stocks.schemas import PageQuery, StockDataset, StockPage
from stock_vision.stocks.service import browse_stocks
from stock_vision.stocks.source import load_sample_stocks

router = APIRouter(prefix="/api/stocks", tags=["stocks"])


@router.get("")
def read_stocks(
    page: Annotated[PageQuery, Query()],
    source: Annotated[StockDataset, Depends(load_sample_stocks)],
) -> StockPage:
    return browse_stocks(source, page)
